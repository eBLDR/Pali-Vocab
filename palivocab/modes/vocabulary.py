from palivocab.helpers import utils
from palivocab.modes.base import ModeBase


class ModeVocabulary(ModeBase):
    """
    Vocabulary from Pāli textbooks
    """

    def __init__(self):
        super().__init__()

    def ask_term(self):
        utils.clear_screen()
        utils.dash_line()
        word = self.unasked_words[0]

        answer = utils.get_user_input(
            prompt='Trans.',
            info=(
                f'Question {self.current_question} of {self.total_questions}'
                f'\n\n{word.original}'
            )
        )

        self.assess_answer(answer, word.translations, word)

    def show_terms_to_review(self):
        print()
        for word in self.words_to_review:
            print(f'{word.original} -> {", ".join(word.translations)}')
