from palivocab.words.inflections.declensions.cases.base import BaseCase
from palivocab.words.inflections.declensions.number.plural import NumberPlural
from palivocab.words.inflections.declensions.number.singular import NumberSingular


class CaseDative(BaseCase):
    singular = NumberSingular(
        stem_a_masculine=['āya', 'assa'],
        stem_a_neuter=['āya', 'assa'],
    )

    plural = NumberPlural(
        stem_a_masculine=['ānaṃ'],
        stem_a_neuter=['ānaṃ'],
    )
