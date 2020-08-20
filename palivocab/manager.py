import random

from palivocab import config, tools
from palivocab.csv_manager import CSVManager
from palivocab.score import Score


class Manager:

    # Vocabulary from Pāli textbooks
    sources = [
        'silva',
        'warder',
    ]

    # Word classes
    word_class_all = 'all'

    word_class_types = [
        word_class_all,
        'verbs',
        'nouns',
        'indeclinables',
        'pronouns',
    ]

    def __init__(self):
        self.csv_manager = CSVManager()

        self.source = None
        self.word_class = None
        self.data_set = {}

        self.total_questions = 0
        self.current_question = 1
        self.unasked_terms = []
        self.score = Score()

        self.terms_to_review = []

    def run(self):
        self.intro()

        self.init_source()
        self.init_mode()
        self.init_data_set()
        self.init_number_of_questions()

        tools.dash_line()
        self.display_set_up()
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

    def init_source(self):
        print(f'Sources (textbook\'s author): '
              f'{", ".join([source.title() for source in self.sources])}')
        while (source := input('Source: ').lower()) not in self.sources:
            continue
        self.source = source

    def init_mode(self):
        print(f'Word classes: '
              f'{", ".join(self.word_class_types)}')
        while (word_class := input('Word class: ').lower()) not in self.word_class_types:
            continue
        self.word_class = word_class

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
        if self.word_class == self.word_class_all:
            for word_class in self.word_class_types:
                if word_class != self.word_class_all:
                    self.data_set.update(
                        self.csv_manager.get_data_set(self.source, word_class)
                    )
        else:
            self.data_set = self.csv_manager.get_data_set(self.source, self.word_class)

        self.unasked_terms = list(self.data_set.keys())
        random.shuffle(self.unasked_terms)

    def display_set_up(self):
        print(f'Loaded {self.total_questions} questions of word class '
              f'{self.word_class} from source {self.source.title()}')

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
