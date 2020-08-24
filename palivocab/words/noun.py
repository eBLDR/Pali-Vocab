from palivocab.words.word import Word


class Noun(Word):
    word_class = 'noun'

    _stems_type = [
        '-a', '-ā',
        '-i', '-ī', '-in',
        '-u', '-ū',
        '-r',
        '-an', '-ant',
        '-as', '-us',
    ]

    _genders_type = [
        ('masculine', 'm.',),
        ('feminine', 'f.',),
        ('neuter', 'nt.'),
    ]

    def __init__(self, original, translations):
        super().__init__(original, translations)

        self.gender = None

    def get_stem(self):
        pass
