from palivocab.words.inflections.declensions.cases.base import BaseCase
from palivocab.words.inflections.declensions.number.plural import NumberPlural
from palivocab.words.inflections.declensions.number.singular import NumberSingular


class CaseGenitive(BaseCase):
    singular = NumberSingular(
        stem_a_masculine=['assa'],
        stem_a_neuter=['assa'],
    )

    plural = NumberPlural(
        stem_a_masculine=['ānaṃ'],
        stem_a_neuter=['ānaṃ'],
    )
