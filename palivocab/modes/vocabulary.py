import random

from palivocab import config, utils
from palivocab.data_manager import DataManager
from palivocab.helpers.score import Score
from palivocab.helpers.word_set import WordSet


class ModeVocabulary:
    """
    Vocabulary from Pāli textbooks
    """

    def __init__(self):
        self.csv_manager = DataManager()

        self.source = None
        self.word_class = None
        self.lesson_number = None
        self.word_set = WordSet()

        self.total_questions = 0
        self.current_question = 1
        self.unasked_terms = []
        self.score = Score()

        self.terms_to_review = []

    def run(self):
        self.set_up()

        utils.dash_line()
        self.display_set_up()
        utils.press_enter_(text='Ready?')

        while self.unasked_terms:
            self.ask_term()
            self.current_question += 1

        utils.clear_screen()
        utils.dash_line()
        utils.press_enter_(text='Finished, see score...')
        self.score.display()

        if self.terms_to_review:
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
            info=(
                f'Sources (textbook\'s author): '
                f'{", ".join([source.title() for source in available_sources])}'
            )
        )

    def init_lesson(self):
        available_lessons = sorted(self.csv_manager.get_available_lessons(self.source))

        # TODO: implement multiple lesson selection
        # print(f'Lessons (comma separated) [all]: {", ".join(available_lessons)}')

        self.lesson_number = utils.get_user_input(
            prompt='Lesson',
            valid_options=available_lessons + [config.ALL_STRING],
            info=f'Lessons [all]: {", ".join(available_lessons)}'
        )

    def init_word_class(self):
        available_word_classes = sorted(self.csv_manager.get_available_word_classes(
            self.source,
            lesson_number=self.lesson_number,
        ))

        self.word_class = utils.get_user_input(
            prompt='Word class',
            valid_options=available_word_classes + [config.ALL_STRING],
            info=f'Word classes [all]: {", ".join(available_word_classes)}'
        )

    def load_data(self):
        self.word_set.add_words(self.csv_manager.generate_words_list(
            self.source,
            lesson_number=self.lesson_number,
            word_class=self.word_class,
        ))

    def init_questions(self):
        original_terms = self.word_set.get_list_of_original_terms()
        random.shuffle(original_terms)

        self.total_questions = utils.get_user_input_integer(
            prompt='Number of questions [blank for max]',
            max_value=len(original_terms),
        )

        self.unasked_terms = original_terms[:self.total_questions]

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
        print(f'Question {self.current_question} of {self.total_questions}\n')
        original_term = self.unasked_terms[0]
        print(original_term)

        answer = utils.get_user_input(prompt='Trans.')

        self.assess_answer(original_term, answer)
        self.unasked_terms.remove(original_term)

    def assess_answer(self, original_term, answer):
        correct_answers = self.word_set.get_translations(original_term)
        is_answer_valid = self.is_answer_valid(answer, correct_answers)

        if is_answer_valid:
            # print('\nCorrect!\n')
            self.score.correct += 1
        else:
            print(f'\nIncorrect. Possible translations: {correct_answers}\n')
            self.score.incorrect += 1
            self.terms_to_review.append(original_term)
            utils.press_enter_(text='Next...')

        self.score.total += 1

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

    def show_terms_to_review(self):
        print()
        for term in self.terms_to_review:
            print(f'{term} -> {", ".join(self.word_set.get_translations(term))}')
