import csv
import os

from palivocab import config
from palivocab.words.word import Word


class DataManager:

    gender_mapper = {
        'm': 'masculine',
        'f': 'feminine',
        'nt': 'neuter',
    }

    def generate_path(self, source=None, lesson_number=None, word_class=None):
        path = os.path.join(
            config.SRC_PATH,
            source.lower() if source else '',
            self.generate_lesson_folder_name(lesson_number) if lesson_number else '',
            self.generate_word_class_file_name(word_class) if word_class else '',
        )

        if not os.path.exists(path):
            raise FileNotFoundError

        return path

    def get_available_sources(self):
        return [
            folder for folder in os.listdir(
                self.generate_path(),
            )
        ]

    def get_available_lessons(self, source):
        return [
            folder.lstrip('lesson0') for folder in os.listdir(
                self.generate_path(
                    source,
                ),
            )
        ]

    def get_available_word_classes(self, source, lesson_number):
        def get_available_word_classes_(source_, lesson_number__):
            return [
                file.replace(config.CSV_EXTENSION, '') for file in os.listdir(
                    self.generate_path(
                        source_,
                        lesson_number=lesson_number__,
                    ),
                )
            ]

        word_classes = set()

        if lesson_number == config.ALL_STRING:
            for lesson_number_ in self.get_available_lessons(source):
                word_classes.update(
                    get_available_word_classes_(source, lesson_number_)
                )

        else:
            word_classes.update(
                get_available_word_classes_(source, lesson_number)
            )

        return word_classes

    def generate_words_list(self, source, lesson_number=None, word_class=None):
        words = []

        available_lesson_numbers = self.get_available_lessons(source)

        if lesson_number == config.ALL_STRING:
            for lesson_number_ in available_lesson_numbers:
                words.extend(
                    self.load_lesson(
                        source,
                        lesson_number=lesson_number_,
                        word_class=word_class,
                    )
                )

        elif lesson_number in available_lesson_numbers:
            words.extend(
                self.load_lesson(
                    source,
                    lesson_number=lesson_number,
                    word_class=word_class,
                )
            )

        return words

    def load_lesson(self, source, lesson_number, word_class=None):
        lesson_words = []

        available_word_classes = self.get_available_word_classes(
            source,
            lesson_number=lesson_number,
        )

        if word_class == config.ALL_STRING:
            for word_class_ in available_word_classes:
                lesson_words.extend(
                    self.load_word_class(
                        source,
                        lesson_number=lesson_number,
                        word_class=word_class_,
                    )
                )

        elif word_class in available_word_classes:
            lesson_words = self.load_word_class(
                source,
                lesson_number=lesson_number,
                word_class=word_class,
            )

        return lesson_words

    def load_word_class(self, source, lesson_number=None, word_class=None):
        file_path = self.generate_path(
            source,
            lesson_number=lesson_number,
            word_class=word_class,
        )

        return self.prepare_data_set(
            self.load_csv(file_path),
            word_class=word_class,
        )

    @staticmethod
    def load_csv(filepath):
        with open(filepath, 'r') as csv_file:
            raw_data = [
                row for row in csv.reader(csv_file)
            ]

        return raw_data

    def prepare_data_set(self, raw_data, word_class=None):
        words = []

        for row in raw_data:
            if word_class == 'nouns':
                original_term, translations, gender = str(row[0]), row[2:], self.gender_mapper.get(row[1])
            else:
                gender = None
                original_term, translations = str(row[0]), row[1:]

            if original_term in words:
                continue

            words.append(
                Word.factory_from_word_class(
                    word_class=word_class,
                    original=original_term,
                    translations=translations,
                    gender=gender,
                )
            )

        return words

    @staticmethod
    def generate_lesson_folder_name(lesson_number: int) -> str:
        lesson_string = str(lesson_number)

        if len(lesson_string) == 1:
            lesson_string = f'0{lesson_string}'

        return config.LESSON_FOLDER_NAME.format(
            two_digit_number=lesson_string,
        )

    @staticmethod
    def generate_word_class_file_name(word_class: str) -> str:
        return word_class + config.CSV_EXTENSION
