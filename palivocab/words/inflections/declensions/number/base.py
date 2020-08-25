from palivocab.words.inflections.declensions.stems.stem_a import StemA


class NumberBase:

    def __init__(
            self,
            stem_a_masculine=None,
            stem_a_neuter=None,
    ):
        self.stem_a = StemA(
            masculine=stem_a_masculine,
            neuter=stem_a_neuter,
        )

    def get_suffixes(self, stem, gender):
        if stem_attribute := getattr(self, f'stem_{stem}'):
            if suffixes := getattr(stem_attribute, gender):
                return suffixes

        return []
