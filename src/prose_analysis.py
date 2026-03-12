from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from functools import lru_cache
import ssl
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from lxml import html

try:
    import certifi
except ModuleNotFoundError:
    certifi = None

def get_average_word_length(text):
    sentences = word_tokenize(text)
    total_words = len(sentences)
    total_characters = sum(len(word) for word in sentences)
    average_word_length = total_characters / total_words if total_words > 0 else 0
    return average_word_length

def get_tokens_per_newline(text):
    lines = text.split('\n')
    if not lines:
        lines = sent_tokenize(text)
    total_tokens = sum(len(word_tokenize(line)) for line in lines)
    tokens_per_newline = total_tokens / len(lines) if lines else 0
    return tokens_per_newline

def get_vocabulary_richness_to_word_count_ratio(text):
    words = word_tokenize(text)
    unique_words = set(words)
    vocabulary_richness = len(unique_words) / len(words) if words else 0
    return vocabulary_richness

def get_latinate_to_germanic_ratio(text):
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.isalpha() and word.lower() not in stop_words]
    if not words:
        return 0.0

    counts = Counter(word.lower() for word in words)
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
        return float("inf") if latinate_count > 0 else 0.0

    return latinate_count / germanic_count

def _classify_origin_text(origin_text):
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

def _get_ssl_context():
    if certifi is not None:
        return ssl.create_default_context(cafile=certifi.where())
    return ssl.create_default_context()

def _fetch_etymonline_entry(word, timeout=10):
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
                paragraph_text = " ".join(t.strip() for t in node.xpath(".//text()") if t.strip())
                if paragraph_text:
                    candidate_paragraphs.append(paragraph_text)

            snippet = ""
            for paragraph in candidate_paragraphs:
                lowered = paragraph.lower()
                if any(
                    marker in lowered
                    for marker in [
                        "old english",
                        "proto-germanic",
                        "latin",
                        "french",
                        "from pie",
                        "from pie root",
                    ]
                ):
                    snippet = paragraph
                    break

            if not snippet:
                snippet = " ".join(candidate_paragraphs[:2])

            snippet = snippet[:1000]
            return url, snippet
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
                        paragraph_text = " ".join(t.strip() for t in node.xpath(".//text()") if t.strip())
                        if paragraph_text:
                            candidate_paragraphs.append(paragraph_text)

                    snippet = ""
                    for paragraph in candidate_paragraphs:
                        lowered = paragraph.lower()
                        if any(
                            marker in lowered
                            for marker in [
                                "old english",
                                "proto-germanic",
                                "latin",
                                "french",
                                "from pie",
                                "from pie root",
                            ]
                        ):
                            snippet = paragraph
                            break

                    if not snippet:
                        snippet = " ".join(candidate_paragraphs[:2])

                    snippet = snippet[:1000]
                    return url, snippet
                except (HTTPError, URLError, OSError, ValueError) as insecure_exc:
                    last_error = insecure_exc

    raise RuntimeError(f"Unable to fetch etymology for '{word}': {last_error}")

@lru_cache(maxsize=4096)
def _lookup_word_origin(word):
    normalized_word = word.strip().lower()

    # Primary attempt: local ety package, but do not hard-fail if dependency is broken.
    try:
        import ety

        origins = ety.origins(normalized_word)
        origin_text = " ".join(str(item) for item in origins) if origins else ""
        return {
            "word": normalized_word,
            "origin_group": _classify_origin_text(origin_text),
            "origin_text": origin_text,
            "source": "ety",
            "url": None,
        }
    except Exception:
        pass

    # Fallback: fetch and classify Etymonline text.
    url, snippet = _fetch_etymonline_entry(normalized_word)
    return {
        "word": normalized_word,
        "origin_group": _classify_origin_text(snippet),
        "origin_text": snippet,
        "source": "etymonline",
        "url": url,
    }

def check_word_origin(word, verbose=True):
    result = _lookup_word_origin(word)
    if verbose:
        print(
            f"Word: {result['word']} | Origin Group: {result['origin_group']} "
            f"| Source: {result['source']}"
        )
        if result["url"]:
            print(f"URL: {result['url']}")
        preview = result["origin_text"][:220].replace("\n", " ").strip()
        print(f"Evidence: {preview}...")
    return result

