class Score:
    def __init__(self):
        self.total = 0
        self.correct = 0
        self.incorrect = 0

    def increase_correct(self):
        self.correct += 1
        self.total += 1

    def increase_incorrect(self):
        self.incorrect += 1
        self.total += 1

    def display(self):
        print(
            f'Correct: {self.correct}/{self.total} ({round(self.correct / self.total * 100, 2)}%)\n'
            f'Incorrect: {self.incorrect}/{self.total} ({round(self.incorrect / self.total * 100, 2)}%)\n'
        )
