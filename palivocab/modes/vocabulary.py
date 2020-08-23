import random

from palivocab import config, utils
from palivocab.helpers.word_set import WordSet
from palivocab.modes.base import ModeBase


class ModeVocabulary(ModeBase):
    """
    Vocabulary from Pāli textbooks
    """

    def __init__(self):
        super().__init__()

        self.source = None
        self.word_class = None
        self.lesson_number = None

        self.word_set = WordSet()

        self.total_questions = 0
        self.current_question = 1
        self.unasked_words = []

        self.words_to_review = []

    def run(self):
        self.set_up()

        utils.dash_line()
        self.display_set_up()
        utils.press_enter_(text='Ready?')

        while self.unasked_words:
            self.ask_term()
            self.current_question += 1

        utils.clear_screen()
        utils.dash_line()
        utils.press_enter_(text='Finished, see score...')
        self.score.display()

        if self.words_to_review:
            utils.dash_line()
            utils.press_enter_(text='Incorrect answers for reviewing...')
            self.show_terms_to_review()

        utils.dash_line()
        utils.press_enter_(text='Done!')

    def set_up(self):
        self.init_source()
        self.init_lesson()
        self.init_word_class()
        self.load_data()
        self.init_questions()

    def init_source(self):
        available_sources = sorted(self.csv_manager.get_available_sources())

        self.source = utils.get_user_input(
            prompt='Source',
            valid_options=available_sources,
            info=f'Sources (textbook\'s author)',
        )

    def init_lesson(self):
        available_lessons = sorted(self.csv_manager.get_available_lessons(self.source))

        # TODO: implement multiple lesson selection
        # print(f'Lessons (comma separated) [all]: {", ".join(available_lessons)}')

        self.lesson_number = utils.get_user_input(
            prompt='Lesson',
            valid_options=available_lessons + [config.ALL_STRING],
            info=f'Lessons',
        )

    def init_word_class(self):
        available_word_classes = sorted(self.csv_manager.get_available_word_classes(
            self.source,
            lesson_number=self.lesson_number,
        ))

        self.word_class = utils.get_user_input(
            prompt='Word class',
            valid_options=available_word_classes + [config.ALL_STRING],
            info=f'Word classes',
        )

    def load_data(self):
        self.word_set.add_words(self.csv_manager.generate_words_list(
            self.source,
            lesson_number=self.lesson_number,
            word_class=self.word_class,
        ))

    def init_questions(self):
        random.shuffle(self.word_set.words)

        self.total_questions = utils.get_user_input_integer(
            prompt='Number of questions [blank for max]',
            max_value=len(self.word_set.words),
        )

        self.unasked_words = self.word_set.words[:self.total_questions]

    def display_set_up(self):
        print(
            f'Loaded.\n'
            f'Source: {self.source.title()}\n'
            f'Lesson: {self.lesson_number}\n'
            f'Word class: {self.word_class}\n'
            f'Questions: {self.total_questions}'
        )

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

        self.assess_answer(word, answer)
        self.unasked_words.remove(word)

    def assess_answer(self, word, answer):
        is_answer_valid = self.is_answer_valid(
            answer,
            word.translations,
        )

        if is_answer_valid:
            # print('\nCorrect!\n')
            self.score.add_correct()

        else:
            print(f'\nIncorrect. Possible answers: {word.translations}\n')
            self.score.add_incorrect()
            self.words_to_review.append(word)
            utils.press_enter_(text='Next...')

        self.score.total += 1

    def show_terms_to_review(self):
        print()
        for word in self.words_to_review:
            print(f'{word.original} -> {", ".join(word.translations)}')
