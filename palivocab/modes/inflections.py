from palivocab.helpers import utils
from palivocab.helpers.word_set import WordSet
from palivocab.modes.base import ModeBase


class ModeInflections(ModeBase):
    """
    Inflections of Pāli terms
    """

    def __init__(self):
        super().__init__()

        self.sub_mode = None

        self.word_set = WordSet()

    # Overriding parent method - inflection only accepts nouns and verbs
    def init_word_class(self):
        self.word_class = utils.get_user_input(
            prompt='Word class',
            info=f'Inflection of',
            valid_options=['nouns'],
            accept_shortcuts=True,
        )

    def ask_term(self):
        utils.clear_screen()
        utils.dash_line()
        word = self.unasked_words[0]

        # for loop iterating over cases / numbers
            # answer = utils.get_user_input(
            #     prompt='Trans.',
            #     info=(
            #         f'Question {self.current_question} of {self.total_questions}'
            #         f'\n\n{word.original}'
            #     )
            # )
            #
            # self.assess_answer(answer, word.declensions, word)
        print(word.declensions)

    def show_terms_to_review(self):
        pass
