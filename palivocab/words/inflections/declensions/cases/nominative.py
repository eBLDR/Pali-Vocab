from palivocab.words.inflections.declensions.cases.base import BaseCase
from palivocab.words.inflections.declensions.number.singular import NumberSingular
from palivocab.words.inflections.declensions.number.plural import NumberPlural


class CaseNominative(BaseCase):
    singular = NumberSingular(
        stem_a_masculine=['o'],
        stem_a_neuter=['aṃ'],
    )

    plural = NumberPlural(
        stem_a_masculine=['ā'],
        stem_a_neuter=['āni', 'ā'],
    )
