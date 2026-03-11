from nltk import sent_tokenize, word_tokenize

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
    latinate_words = set()
    germanic_words = set()
    with open('latinate_words.txt') as f:
        for line in f:
            latinate_words.add(line.strip().lower())
    with open('germanic_words.txt') as f:
        for line in f:
            germanic_words.add(line.strip().lower())
    words = word_tokenize(text)
    latinate_count = sum(1 for word in words if word.lower() in latinate_words)
    germanic_count = sum(1 for word in words if word.lower() in germanic_words)
    ratio = (latinate_count / germanic_count) if germanic_count > 0 else float('inf')
    return ratio