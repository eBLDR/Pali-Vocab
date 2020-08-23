class WordSet:
    def __init__(self):
        self.words = []

    def add_words(self, words):
        self.words.extend(words)

    def get_translations(self, original):
        for word in self.words:
            if word.original == original:
                return word.translations

    def get_list_of_original_terms(self):
        original_terms = []

        for word in self.words:
            original_terms.append(word.original)

        return original_terms
