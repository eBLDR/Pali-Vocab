from palivocab.words.word import Word


class Verb(Word):
    word_class = 'verb'

    def __init__(self, original, translations):
        super().__init__(original, translations)
