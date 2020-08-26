from palivocab.words.inflections.declensions.cases.base import BaseCase
from palivocab.words.inflections.declensions.number.plural import NumberPlural
from palivocab.words.inflections.declensions.number.singular import NumberSingular


class CaseLocative(BaseCase):
    singular = NumberSingular(
        stem_a_masculine=['e', 'asmiṃ', 'amhi'],
        stem_a_neuter=['e', 'asmiṃ', 'amhi'],
    )

    plural = NumberPlural(
        stem_a_masculine=['esu'],
        stem_a_neuter=['esu'],
    )
