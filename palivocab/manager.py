import random

from palivocab import config, tools
from palivocab.csv_manager import CSVManager
from palivocab.score import Score


class Manager:
    """
    Vocabulary from Pāli textbooks
    """

    def __init__(self):
        self.csv_manager = CSVManager()

        self.source = None
        self.word_class = None
        self.lesson_number = None
        self.data_set = {}

        self.total_questions = 0
        self.current_question = 1
        self.unasked_terms = []
        self.score = Score()

        self.terms_to_review = []

    def run(self):
        self.intro()

        self.set_up()

        tools.dash_line()
        self.display_set_up()
        tools.press_enter_(text='Ready?')

        while self.unasked_terms:
            self.ask_term()
            self.current_question += 1

        tools.clear_screen()
        tools.dash_line()
        tools.press_enter_(text='Finished, see score...')
        self.score.display()

        if self.terms_to_review:
            tools.dash_line()
            tools.press_enter_(text='Incorrect answers for reviewing...')
            self.show_terms_to_review()

        tools.dash_line()
        tools.press_enter_(text='Done!')

    @staticmethod
    def intro():
        tools.clear_screen()
        print(
            f'{config.PROJECT_NAME}\n\nNotes (unless otherwise specified):\n'
            '\t- Verbs are given in the 3r person singular form\n'
            '\t- Nouns are given in the stem form, translated as the '
            'nominative case 1st person singular form\n'
        )
        tools.dash_line()

    def set_up(self):
        self.init_source()
        self.init_lesson()
        self.init_word_class()
        self.load_data()
        self.init_questions()

    def init_source(self):
        available_sources = sorted(self.csv_manager.get_available_sources())
        print(f'Sources (textbook\'s author): '
              f'{", ".join([source.title() for source in available_sources])}')

        self.source = tools.get_user_input(
            prompt='Source',
            valid_options=available_sources,
        )

    def init_word_class(self):
        available_word_classes = self.csv_manager.get_available_word_classes(
            self.source,
            lesson_number=self.lesson_number,
        )
        print(f'Word classes [all]: {", ".join(available_word_classes)}')

        self.word_class = tools.get_user_input(
            prompt='Word class',
            valid_options=available_word_classes + [config.ALL_STRING],
        )

    def init_lesson(self):
        available_lessons = self.csv_manager.get_available_lessons(self.source)
        print(f'Lessons: {", ".join(available_lessons)}')

        # TODO: implement multiple lesson selection & `all` selection
        # print(f'Lessons (comma separated) [all]: {", ".join(available_lessons)}')

        self.lesson_number = tools.get_user_input(
            prompt='Lesson',
            valid_options=available_lessons,  # + [config.ALL_STRING],
        )

    def load_data(self):
        self.data_set = self.csv_manager.generate_data_set(
            self.source,
            lesson_number=self.lesson_number,
            word_class=self.word_class,
        )

    def init_questions(self):
        original_terms = list(self.data_set.keys())
        random.shuffle(original_terms)

        self.total_questions = tools.get_user_input_integer(
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
        tools.clear_screen()
        tools.dash_line()
        print(f'Question {self.current_question} of {self.total_questions}\n')
        original_term = self.unasked_terms[0]
        print(original_term)

        answer = tools.get_user_input(prompt='Trans.')

        self.assess_answer(original_term, answer)
        self.unasked_terms.remove(original_term)

    def assess_answer(self, original_term, answer):
        correct_answers = self.data_set[original_term]
        is_answer_valid = self.is_answer_valid(correct_answers, answer)

        if is_answer_valid:
            # print('\nCorrect!\n')
            self.score.correct += 1
        else:
            print(f'\nIncorrect. Possible translations: {correct_answers}\n')
            self.score.incorrect += 1
            self.terms_to_review.append(original_term)
            tools.press_enter_(text='Next...')

        self.score.total += 1

    @staticmethod
    def is_answer_valid(correct_answers, answer):
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
            print(f'{term} -> {", ".join(self.data_set[term])}')
