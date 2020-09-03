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
        available_word_classes = ['nouns']  # TMP

        self.selected_word_classes = utils.get_user_input(
            prompt='Word class',
            info=f'Inflection of',
            valid_options=available_word_classes,
            accept_shortcuts=True,
        )

    def ask_term(self):
        utils.clear_screen()
        utils.dash_line()
        noun = self.unasked_words[0]

        print(
            f'Question {self.current_question} of {self.total_questions}'
            f'\nNoun: {noun.original}\n'
        )

        for case, singular_forms, plural_forms in noun.declensions.declined_forms:
            for number, declensions in zip(
                    ('sing.', 'pl.'),
                    (singular_forms, plural_forms),
            ):
                answer = utils.get_user_input(prompt=f'{case} {number}')
                self.assess_answer(answer, declensions, noun, remove=False)

        self.unasked_words.remove(noun)
        utils.press_enter_(text='Noun completed. Next')

    def show_terms_to_review(self):
        print()
        for noun in self.words_to_review:
            print(noun.declensions)
