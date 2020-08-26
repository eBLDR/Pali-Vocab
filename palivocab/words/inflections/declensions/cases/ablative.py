from palivocab.words.inflections.declensions.cases.base import BaseCase
from palivocab.words.inflections.declensions.number.plural import NumberPlural
from palivocab.words.inflections.declensions.number.singular import NumberSingular


class CaseAblative(BaseCase):
    singular = NumberSingular(
        stem_a_masculine=['ā', 'asmā', 'amhā', 'ato'],
        stem_a_neuter=['ā', 'asmā', 'amhā', 'ato'],
    )

    plural = NumberPlural(
        stem_a_masculine=['ehi', 'ebhi'],
        stem_a_neuter=['ehi'],
    )
