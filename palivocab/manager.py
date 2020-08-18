import random

from palivocab import config, tools
from palivocab.csv_manager import CSVManager
from palivocab.score import Score


class Manager:
    word_class_all = 'all'
    word_class_verbs = 'verbs'
    word_class_nouns = 'nouns'
    word_class_indeclinables = 'indeclinables'
    word_class_pronouns = 'pronouns'

    word_class_types = [
        word_class_all,
        word_class_verbs,
        word_class_nouns,
        word_class_indeclinables,
        word_class_pronouns,
    ]

    def __init__(self):
        self.csv_manager = CSVManager()

        self.mode = None
        self.data_set = {}

        self.total_questions = 0
        self.current_question = 1
        self.unasked_terms = []
        self.score = Score()

        self.terms_to_review = []

    def run(self):
        self.intro()

        self.init_mode()
        self.init_data_set()
        self.init_number_of_questions()

        tools.dash_line()
        tools.press_enter_(text='Ready?')

        while self.current_question <= self.total_questions:
            self.ask_term()
            self.current_question += 1
            tools.press_enter_()

        tools.clear_screen()
        tools.dash_line()
        tools.press_enter_(text='Done, see score...')
        self.score.display()

        if self.terms_to_review:
            tools.dash_line()
            tools.press_enter_(text='Incorrect answers for reviewing...')
            self.show_terms_to_review()

    @staticmethod
    def intro():
        tools.clear_screen()
        print(f'{config.PROJECT_NAME}\n')

    def init_mode(self):
        print(f'Modes: {self.word_class_types}')
        while (mode := input('Mode: ').lower()) not in self.word_class_types:
            continue
        self.mode = mode

    def init_number_of_questions(self):
        max_ = len(self.unasked_terms)
        while True:
            questions = input(f'Number of questions (max. {max_}): ')
            if questions.isdigit():
                questions = int(questions)
                if 0 < questions <= max_:
                    break

        self.total_questions = questions

    def init_data_set(self):
        if self.mode == self.word_class_all:
            for word_class in self.word_class_types:
                if word_class != self.word_class_all:
                    self.data_set.update(
                        self.csv_manager.get_data_set(word_class)
                    )
        else:
            self.data_set = self.csv_manager.get_data_set(self.mode)

        self.unasked_terms = list(self.data_set.keys())
        random.shuffle(self.unasked_terms)

    def ask_term(self):
        tools.clear_screen()
        tools.dash_line()
        print(f'Question {self.current_question} of {self.total_questions}\n')
        original_term = self.unasked_terms[0]
        print(original_term)

        while True:
            answer = input('Trans.: ')
            if answer:
                break

        self.assess_answer(original_term, answer)
        self.unasked_terms.remove(original_term)

    def assess_answer(self, original_term, answer):
        correct_answers = self.data_set[original_term]
        is_answer_valid = self.is_answer_valid(correct_answers, answer)

        if is_answer_valid:
            print('\nCorrect!\n')
            self.score.correct += 1
        else:
            print(f'\nIncorrect. Possible translations: {correct_answers}\n')
            self.score.incorrect += 1
            self.terms_to_review.append(original_term)

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
