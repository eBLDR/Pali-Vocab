import random

from palivocab.data_manager import DataManager
from palivocab.helpers import utils
from palivocab.helpers.score import Score
from palivocab.helpers.word_set import WordSet


class ModeBase:
    def __init__(self):
        self.csv_manager = DataManager()
        self.word_set = WordSet()
        self.score = Score()

        self.source = None
        self.selected_word_classes = None
        self.selected_lessons = None

        self.total_questions = 0
        self.current_question = 1
        self.unasked_words = []

        self.words_to_review = set()

    def run(self):
        while True:
            self.set_up()

            if utils.confirmation():
                break

        while self.unasked_words:
            self.ask_term()
            self.current_question += 1

        utils.clear_screen()
        utils.dash_line()
        utils.press_enter(text='Finished, see score...')
        self.score.display()

        if self.words_to_review:
            utils.dash_line()
            utils.press_enter(text='Incorrect answers for reviewing...')
            self.show_terms_to_review()

        utils.dash_line()
        utils.press_enter(text='Done!')

    def set_up(self):
        self.init_source()
        self.init_lesson()
        self.init_word_class()
        self.load_data()
        self.init_questions()

        utils.dash_line()
        self.display_set_up()

    def init_source(self):
        available_sources = sorted(self.csv_manager.get_available_sources())

        self.source = utils.get_user_input(
            prompt='Source',
            info=f'Sources (textbook\'s author)',
            valid_options=available_sources,
            accept_shortcuts=True,
        )

    def init_lesson(self):
        available_lessons = self.csv_manager.get_available_lessons(self.source)

        self.selected_lessons = utils.get_user_input(
            prompt='Lesson',
            info=f'Lessons',
            valid_options=available_lessons,
            accept_many=True,
        )

    def init_word_class(self):
        available_word_classes = set()

        for lesson_number in self.selected_lessons:
            available_word_classes.update(
                self.csv_manager.get_available_word_classes(
                    self.source,
                    lesson_number=lesson_number,
                )
            )

        self.selected_word_classes = utils.get_user_input(
            prompt='Word class',
            info=f'Word classes',
            valid_options=sorted(list(available_word_classes)),
            accept_shortcuts=True,
            accept_many=True,
        )

    def load_data(self):
        if not isinstance(self.selected_lessons, list):
            self.selected_lessons = [self.selected_lessons]

        if not isinstance(self.selected_word_classes, list):
            self.selected_word_classes = [self.selected_word_classes]

        self.word_set.clear()

        self.word_set.add_words(
            self.csv_manager.generate_words_list(
                self.source,
                self.selected_lessons,
                self.selected_word_classes,
            )
        )

    def init_questions(self):
        random.shuffle(self.word_set)

        self.total_questions = utils.get_user_input_integer(
            prompt='Number of questions [blank for max]',
            max_value=len(self.word_set),
        )

        self.unasked_words = self.word_set[:self.total_questions]

    def display_set_up(self):
        print(
            f'Loaded.\n'
            f'Source: {self.source.title()}\n'
            f'Lessons: {self.selected_lessons}\n'
            f'Word classes: {self.selected_word_classes}\n'
            f'Questions: {self.total_questions}'
        )

    @staticmethod
    def is_answer_valid(answer, correct_answers):
        if answer in correct_answers:
            return True

        # Asses terms without case sensitivity
        if answer.lower() in [correct_answer.lower() for correct_answer in correct_answers]:
            return True

        # Asses terms with dash (-)
        if answer.replace(' ', '-') in correct_answers:
            return True

        return False

    def ask_term(self):
        raise NotImplementedError

    def assess_answer(self, answer, correct_answers, word, remove=True):
        is_answer_valid = self.is_answer_valid(
            answer,
            correct_answers,
        )

        if is_answer_valid:
            # print('\nCorrect!\n')
            self.score.increase_correct()

        else:
            print(f'\nIncorrect. Possible answers: {correct_answers}\n')
            self.score.increase_incorrect()
            self.words_to_review.add(word)
            utils.press_enter(text='Next...')

        if remove:
            self.unasked_words.remove(word)

    def show_terms_to_review(self):
        raise NotImplementedError
