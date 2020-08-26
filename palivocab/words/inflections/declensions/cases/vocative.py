from palivocab.words.inflections.declensions.cases.base import BaseCase
from palivocab.words.inflections.declensions.number.plural import NumberPlural
from palivocab.words.inflections.declensions.number.singular import NumberSingular


class CaseVocative(BaseCase):
    singular = NumberSingular(
        stem_a_masculine=['a', 'ā'],
        stem_a_neuter=['a', 'aṃ'],
    )

    plural = NumberPlural(
        stem_a_masculine=['ā'],
        stem_a_neuter=['āni', 'ā'],
    )
