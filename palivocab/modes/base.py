from palivocab.data_manager import DataManager
from palivocab.helpers.score import Score


class ModeBase:
    def __init__(self):
        self.csv_manager = DataManager()
        self.score = Score()

    def run(self):
        raise NotImplementedError

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


