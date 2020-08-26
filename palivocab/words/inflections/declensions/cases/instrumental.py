from palivocab.words.inflections.declensions.cases.base import BaseCase
from palivocab.words.inflections.declensions.number.plural import NumberPlural
from palivocab.words.inflections.declensions.number.singular import NumberSingular


class CaseInstrumental(BaseCase):
    singular = NumberSingular(
        stem_a_masculine=['ena'],
        stem_a_neuter=['ena'],
    )

    plural = NumberPlural(
        stem_a_masculine=['ehi', 'ebhi'],
        stem_a_neuter=['ehi', 'ebhi'],
    )
