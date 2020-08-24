from palivocab.words.inflections.declensions.declensions import Declensions
from palivocab.words.word import Word


class Noun(Word):
    word_class = 'noun'

    _genders_type = [
        ('masculine', 'm.',),
        ('feminine', 'f.',),
        ('neuter', 'nt.'),
    ]

    def __init__(self, original, translations):
        super().__init__(original, translations)

        self.gender = None

        self.declensions = Declensions(self.original, self.gender)

    def get_stem(self):
        pass
