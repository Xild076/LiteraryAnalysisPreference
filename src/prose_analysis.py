from __future__ import annotations

import math
import re
import sqlite3
import ssl
from collections import Counter
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from lxml import html

try:
    import certifi
except ModuleNotFoundError:
    certifi = None

WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
STOP_WORDS = frozenset(
    {
        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at",
        "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
        "can", "could",
        "did", "do", "does", "doing", "down", "during",
        "each",
        "few", "for", "from", "further",
        "had", "has", "have", "having", "he", "her", "here", "hers", "herself", "him", "himself", "his", "how",
        "i", "if", "in", "into", "is", "it", "its", "itself",
        "just",
        "me", "more", "most", "my", "myself",
        "no", "nor", "not", "now",
        "of", "off", "on", "once", "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own",
        "same", "she", "should", "so", "some", "such",
        "than", "that", "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they", "this", "those", "through", "to", "too",
        "under", "until", "up",
        "very",
        "was", "we", "were", "what", "when", "where", "which", "while", "who", "whom", "why", "will", "with", "would",
        "you", "your", "yours", "yourself", "yourselves",
    }
)
CACHE_PATH = Path(__file__).resolve().parents[1] / "data" / "cache" / "etymology.sqlite"
FAILED_LOOKUPS: set[str] = set()



def _tokenize(text: str) -> list[str]:
    if not isinstance(text, str):
        return []
    return WORD_RE.findall(text)



def _normalize_word(word: str) -> str:
    return re.sub(r"[^a-z]", "", word.lower())



def get_average_word_length(text: str) -> float:
    words = _tokenize(text)
    if not words:
        return 0.0
    return sum(len(word) for word in words) / len(words)



def get_vocabulary_richness_to_word_count_ratio(text: str) -> float:
    words = [_normalize_word(word) for word in _tokenize(text)]
    words = [word for word in words if word]
    if not words:
        return 0.0
    return len(set(words)) / len(words)



def _filtered_words(text: str) -> list[str]:
    words = [_normalize_word(word) for word in _tokenize(text)]
    return [word for word in words if word and word not in STOP_WORDS]



def get_latinate_to_germanic_ratio(text: str) -> float:
    words = _filtered_words(text)
    if not words:
        return 0.0
    counts = Counter(words)
    latinate_count = 0
    germanic_count = 0
    for word, count in counts.items():
        origin_data = check_word_origin(word, verbose=False)
        origin_group = origin_data.get("origin_group", "unknown")
        if origin_group == "latinate":
            latinate_count += count
        elif origin_group == "germanic":
            germanic_count += count
    if germanic_count == 0:
        if latinate_count == 0:
            return 0.0
        return math.nan
    return latinate_count / germanic_count



def compute_poem_features(text: str) -> dict[str, float]:
    return {
        "avg_word_length": get_average_word_length(text),
        "latinate_ratio": get_latinate_to_germanic_ratio(text),
        "type_token_ratio": get_vocabulary_richness_to_word_count_ratio(text),
    }



def _classify_origin_text(origin_text: str) -> str:
    text = origin_text.lower()
    latinate_markers = ["latin", "french", "old french", "anglo-french", "vulgar latin"]
    germanic_markers = ["germanic", "old english", "proto-germanic", "west germanic", "old norse"]
    has_latinate = any(marker in text for marker in latinate_markers)
    has_germanic = any(marker in text for marker in germanic_markers)
    if has_latinate and not has_germanic:
        return "latinate"
    if has_germanic and not has_latinate:
        return "germanic"
    if has_latinate and has_germanic:
        return "mixed"
    return "unknown"



def _get_ssl_context() -> ssl.SSLContext:
    if certifi is not None:
        return ssl.create_default_context(cafile=certifi.where())
    return ssl.create_default_context()



def _ensure_cache() -> sqlite3.Connection:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(CACHE_PATH)
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS etymology_cache (
            word TEXT PRIMARY KEY,
            origin_group TEXT NOT NULL,
            origin_text TEXT NOT NULL,
            source TEXT NOT NULL,
            url TEXT,
            updated_at TEXT NOT NULL
        )
        """
    )
    connection.commit()
    return connection



def _load_cached_origin(word: str) -> dict | None:
    connection = _ensure_cache()
    try:
        row = connection.execute(
            "SELECT word, origin_group, origin_text, source, url, updated_at FROM etymology_cache WHERE word = ?",
            (word,),
        ).fetchone()
    finally:
        connection.close()
    if row is None:
        return None
    return {
        "word": row[0],
        "origin_group": row[1],
        "origin_text": row[2],
        "source": row[3],
        "url": row[4],
        "updated_at": row[5],
    }



def _store_cached_origin(result: dict) -> dict:
    payload = {
        "word": result["word"],
        "origin_group": result["origin_group"],
        "origin_text": result["origin_text"],
        "source": result["source"],
        "url": result.get("url"),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    connection = _ensure_cache()
    try:
        connection.execute(
            """
            INSERT INTO etymology_cache (word, origin_group, origin_text, source, url, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(word) DO UPDATE SET
                origin_group = excluded.origin_group,
                origin_text = excluded.origin_text,
                source = excluded.source,
                url = excluded.url,
                updated_at = excluded.updated_at
            """,
            (
                payload["word"],
                payload["origin_group"],
                payload["origin_text"],
                payload["source"],
                payload["url"],
                payload["updated_at"],
            ),
        )
        connection.commit()
    finally:
        connection.close()
    return payload



def _fetch_etymonline_entry(word: str, timeout: int = 10) -> tuple[str, str]:
    encoded_word = quote(word.strip())
    urls = [
        f"https://www.etymonline.com/word/{encoded_word}",
        f"https://www.etymonline.com/index.php?term={encoded_word}",
    ]
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }
    last_error = None
    for url in urls:
        try:
            request = Request(url, headers=headers)
            with urlopen(request, timeout=timeout, context=_get_ssl_context()) as response:
                page = response.read()
            doc = html.fromstring(page)
            paragraph_nodes = doc.xpath("//main//section//p")
            candidate_paragraphs = []
            for node in paragraph_nodes:
                paragraph_text = " ".join(text.strip() for text in node.xpath(".//text()") if text.strip())
                if paragraph_text:
                    candidate_paragraphs.append(paragraph_text)
            snippet = ""
            for paragraph in candidate_paragraphs:
                lowered = paragraph.lower()
                if any(marker in lowered for marker in ["old english", "proto-germanic", "latin", "french", "from pie", "from pie root"]):
                    snippet = paragraph
                    break
            if not snippet:
                snippet = " ".join(candidate_paragraphs[:2])
            return url, snippet[:1000]
        except (HTTPError, URLError, OSError, ValueError) as exc:
            last_error = exc
            if isinstance(exc, URLError) and "CERTIFICATE_VERIFY_FAILED" in str(exc):
                try:
                    insecure_context = ssl._create_unverified_context()
                    request = Request(url, headers=headers)
                    with urlopen(request, timeout=timeout, context=insecure_context) as response:
                        page = response.read()
                    doc = html.fromstring(page)
                    paragraph_nodes = doc.xpath("//main//section//p")
                    candidate_paragraphs = []
                    for node in paragraph_nodes:
                        paragraph_text = " ".join(text.strip() for text in node.xpath(".//text()") if text.strip())
                        if paragraph_text:
                            candidate_paragraphs.append(paragraph_text)
                    snippet = " ".join(candidate_paragraphs[:2])[:1000]
                    return url, snippet
                except (HTTPError, URLError, OSError, ValueError) as insecure_exc:
                    last_error = insecure_exc
    raise RuntimeError(f"Unable to fetch etymology for '{word}': {last_error}")



def _lookup_with_ety(word: str) -> dict | None:
    try:
        import ety
    except ModuleNotFoundError:
        return None
    try:
        origins = ety.origins(word)
    except Exception:
        return None
    origin_text = " ".join(str(item) for item in origins) if origins else ""
    if not origin_text:
        return None
    return {
        "word": word,
        "origin_group": _classify_origin_text(origin_text),
        "origin_text": origin_text,
        "source": "ety",
        "url": None,
    }



def _unknown_origin(word: str) -> dict:
    return {
        "word": word,
        "origin_group": "unknown",
        "origin_text": "",
        "source": "unavailable",
        "url": None,
    }



def _resolve_origin(word: str, refresh: bool = False) -> dict:
    normalized_word = _normalize_word(word)
    if not normalized_word:
        return _unknown_origin("")
    if not refresh and normalized_word in FAILED_LOOKUPS:
        return _unknown_origin(normalized_word)
    if not refresh:
        cached = _load_cached_origin(normalized_word)
        if cached is not None:
            return cached
    local_origin = _lookup_with_ety(normalized_word)
    if local_origin is not None:
        FAILED_LOOKUPS.discard(normalized_word)
        return _store_cached_origin(local_origin)
    try:
        url, snippet = _fetch_etymonline_entry(normalized_word)
    except RuntimeError:
        FAILED_LOOKUPS.add(normalized_word)
        return _unknown_origin(normalized_word)
    resolved = {
        "word": normalized_word,
        "origin_group": _classify_origin_text(snippet),
        "origin_text": snippet,
        "source": "etymonline",
        "url": url,
    }
    FAILED_LOOKUPS.discard(normalized_word)
    return _store_cached_origin(resolved)


@lru_cache(maxsize=4096)
def _lookup_word_origin(word: str) -> dict:
    return _resolve_origin(word, refresh=False)



def check_word_origin(word: str, verbose: bool = False, refresh: bool = False) -> dict:
    result = _resolve_origin(word, refresh=True) if refresh else _lookup_word_origin(word)
    if verbose:
        print(f"Word: {result['word']} | Origin Group: {result['origin_group']} | Source: {result['source']}")
        if result.get("url"):
            print(f"URL: {result['url']}")
        if result.get("origin_text"):
            preview = result["origin_text"][:220].replace("\n", " ").strip()
            print(f"Evidence: {preview}...")
    return result



def warm_etymology_cache(texts_or_words, refresh: bool = False) -> dict[str, int]:
    unique_words = set()
    for item in texts_or_words:
        if not isinstance(item, str):
            continue
        tokens = _filtered_words(item) if len(item.split()) > 1 else [_normalize_word(item)]
        unique_words.update(word for word in tokens if word)
    cached = 0
    fetched = 0
    unknown = 0
    for word in sorted(unique_words):
        before = None if refresh else _load_cached_origin(word)
        result = check_word_origin(word, verbose=False, refresh=refresh)
        if before is not None and not refresh:
            cached += 1
        elif result["source"] == "unavailable":
            unknown += 1
        else:
            fetched += 1
    return {
        "unique_words": len(unique_words),
        "cached_hits": cached,
        "fetched": fetched,
        "unknown": unknown,
    }
