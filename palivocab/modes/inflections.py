from palivocab.helpers import utils
from palivocab.helpers.word_set import WordSet
from palivocab.modes.base import ModeBase
from palivocab.words import Noun


class ModeInflections(ModeBase):
    """
    Inflections of Pāli terms
    """

    def __init__(self):
        super().__init__()

        # TMP
        self.sub_mode_mapper = {
            'declension': self.run_sub_mode_declension,
            'conjugation': self.run_sub_mode_conjugation,
        }
        self.sub_mode = None

        self.word_set = WordSet()

    def run(self):
        self.init_sub_mode()

        self.load_word_set()

        self.sub_mode_mapper[self.sub_mode]()

    def init_sub_mode(self):
        available_sub_modes = list(self.sub_mode_mapper.keys())
        self.sub_mode = utils.get_user_input(
            prompt='Sub mode',
            info=f'Available sub modes',
            valid_options=available_sub_modes,
            accept_shortcuts=True,
        )

    def load_word_set(self):
        # TMP
        test_word = Noun(
            original='dhamma',
            translations=['doctrine', 'truth'],
            gender='masculine',
        )
        self.word_set.add_words([test_word])

    def run_sub_mode_declension(self):
        for noun in self.word_set:
            print(noun.declensions)

    def run_sub_mode_conjugation(self):
        print('Coming soon')
