from palivocab import config, utils
from palivocab.modes.inflections import ModeInflections
from palivocab.modes.vocabulary import ModeVocabulary


class Manager:
    modes_mapper = {
        'vocabulary': ModeVocabulary,
        'inflections': ModeInflections,
    }

    def __init__(self):
        self.mode = None

    def run(self):
        self.intro()

        self.init_mode()
        if not self.mode:
            raise NotImplementedError

        self.mode.run()

    @staticmethod
    def intro():
        utils.clear_screen()
        print(
            f'{config.PROJECT_NAME}\n\nNotes (unless otherwise specified):\n'
            '\t- Verbs are given in the 3r person singular form of the present tense\n'
            '\t- Nouns are given in the stem form, translated as the '
            'nominative case 1st person singular form\n'
            '\t- Word class `others` include adverbs, prepositions, etc.'
        )
        utils.dash_line()

    def init_mode(self):
        available_modes = list(self.modes_mapper.keys())
        selected_mode = utils.get_user_input(
            prompt='Mode',
            valid_options=available_modes,
            info=f'Available modes',
        )

        self.mode = self.modes_mapper.get(selected_mode)()

