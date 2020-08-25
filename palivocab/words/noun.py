from palivocab.words.inflections.declensions.declensions import Declensions
from palivocab.words.word import Word


class Noun(Word):
    word_class = 'noun'

    _genders_type = [
        'masculine',
        'feminine',
        'neuter',
    ]

    def __init__(self, original, translations, gender=None):
        super().__init__(original, translations)

        self.gender = gender if gender in self._genders_type else None

        self.declensions = Declensions(
            self.original,
            self.gender,
        ) if self.gender else None
