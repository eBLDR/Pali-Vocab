from palivocab.words.inflections.declensions.cases import CaseAblative, CaseAccusative, CaseDative, CaseGenitive, CaseInstrumental, CaseLocative, CaseNominative, CaseVocative
from palivocab.words.inflections.inflections import Inflections


class Declensions(Inflections):
    _stem_types = [
        'a', 'ā',
        'i', 'ī', 'in',
        'u', 'ū',
        'r',
        'an', 'ant',
        'as', 'us',
    ]

    case_nominative = CaseNominative()
    case_vocative = CaseVocative()
    case_accusative = CaseAccusative()
    case_instrumental = CaseInstrumental()
    case_ablative = CaseAblative()
    case_genitive = CaseGenitive()
    case_dative = CaseDative()
    case_locative = CaseLocative()

    def __init__(self, noun, gender):
        super().__init__()

        self.noun = noun
        self.gender = gender

        self.stem_type = self.determine_stem_type()
        self.nominal_base = self.determine_nominal_base()

        self.nominative_singular = None
        self.vocative_singular = None
        self.accusative_singular = None
        self.instrumental_singular = None
        self.ablative_singular = None
        self.genitive_singular = None
        self.dative_singular = None
        self.locative_singular = None

        self.nominative_plural = None
        self.vocative_plural = None
        self.accusative_plural = None
        self.instrumental_plural = None
        self.ablative_plural = None
        self.genitive_plural = None
        self.dative_plural = None
        self.locative_plural = None

        self.generate_all()

    def __repr__(self):
        str_ = f'Noun: {self.noun} ({self.gender})\n\n'

        str_ += f'Nom. sing.:\n'
        str_ += f'  {", ".join(self.nominative_singular)}\n'
        str_ += f'Nom. pl.:\n'
        str_ += f'  {", ".join(self.nominative_plural)}\n'

        str_ += f'Acc. sing.:\n'
        str_ += f'  {", ".join(self.accusative_singular)}\n'
        str_ += f'Acc. pl.:\n'
        str_ += f'  {", ".join(self.accusative_plural)}\n'

        return str_

    def determine_stem_type(self):
        for stem_type in self._stem_types:
            if self.noun.endswith(stem_type):
                return stem_type

    def determine_nominal_base(self):
        return self.noun[:-len(self.stem_type)]

    def build_declension(self, suffixes):
        return [
            self.nominal_base + suffix for suffix in suffixes
        ]

    def generate_all(self):
        self.generate_nominative_singular()
        self.generate_vocative_singular()
        self.generate_accusative_singular()
        self.generate_instrumental_singular()
        self.generate_ablative_singular()
        self.generate_genitive_singular()
        self.generate_dative_singular()
        self.generate_locative_singular()
        self.generate_nominative_plural()
        self.generate_vocative_plural()
        self.generate_accusative_plural()
        self.generate_instrumental_plural()
        self.generate_ablative_plural()
        self.generate_genitive_plural()
        self.generate_dative_plural()
        self.generate_locative_plural()

    def generate_nominative_singular(self):
        self.nominative_singular = self.build_declension(
            self.case_nominative.singular.get_suffixes(
                stem=self.stem_type,
                gender=self.gender,
            )
        )

    def generate_vocative_singular(self):
        self.vocative_singular = None

    def generate_accusative_singular(self):
        self.accusative_singular = self.build_declension(
            self.case_accusative.singular.get_suffixes(
                stem=self.stem_type,
                gender=self.gender,
            )
        )

    def generate_instrumental_singular(self):
        self.instrumental_singular = None

    def generate_ablative_singular(self):
        self.ablative_singular = None

    def generate_genitive_singular(self):
        self.genitive_singular = None

    def generate_dative_singular(self):
        self.dative_singular = None

    def generate_locative_singular(self):
        self.locative_singular = None

    def generate_nominative_plural(self):
        self.nominative_plural = self.build_declension(
            self.case_nominative.plural.get_suffixes(
                stem=self.stem_type,
                gender=self.gender,
            )
        )

    def generate_vocative_plural(self):
        self.vocative_plural = None

    def generate_accusative_plural(self):
        self.accusative_plural = self.build_declension(
            self.case_accusative.plural.get_suffixes(
                stem=self.stem_type,
                gender=self.gender,
            )
        )

    def generate_instrumental_plural(self):
        self.instrumental_plural = None

    def generate_ablative_plural(self):
        self.ablative_plural = None

    def generate_genitive_plural(self):
        self.genitive_plural = None

    def generate_dative_plural(self):
        self.dative_plural = None

    def generate_locative_plural(self):
        self.locative_plural = None
