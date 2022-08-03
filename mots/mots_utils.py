def filter_words(source_words, cb):
    words = list(filter(cb, source_words))
    return words