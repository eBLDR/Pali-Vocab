from palivocab.words.inflections.declensions.cases.base import BaseCase
from palivocab.words.inflections.declensions.number.plural import NumberPlural
from palivocab.words.inflections.declensions.number.singular import NumberSingular


class CaseAccusative(BaseCase):
    singular = NumberSingular(
        stem_a_masculine=['aṃ'],
        stem_a_neuter=['aṃ'],
    )

    plural = NumberPlural(
        stem_a_masculine=['e'],
        stem_a_neuter=['āni', 'e'],
    )
