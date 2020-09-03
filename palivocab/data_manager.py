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
            return False

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
        return [
            file.replace(config.CSV_EXTENSION, '') for file in os.listdir(
                self.generate_path(
                    source,
                    lesson_number=lesson_number,
                ),
            )
        ]

    def generate_words_list(self, source, lessons_number, word_classes):
        words_list = []

        for lesson_number in lessons_number:
            words_list.extend(
                self.load_lesson(
                    source,
                    lesson_number,
                    word_classes,
                )
            )

        return words_list

    def load_lesson(self, source, lesson_number, word_classes):
        words_list = []

        for word_class in word_classes:
            words_list.extend(
                self.load_word_class(
                    source,
                    lesson_number=lesson_number,
                    word_class=word_class,
                )
            )

        return words_list

    def load_word_class(self, source, lesson_number, word_class):
        file_path = self.generate_path(
            source=source,
            lesson_number=lesson_number,
            word_class=word_class,
        )

        if not file_path:
            return []

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
        words_list = []

        for row in raw_data:
            original_term, translations, kwargs = self.extract_row(row, word_class=word_class)

            if original_term in words_list:
                continue

            words_list.append(
                Word.factory_from_word_class(
                    word_class=word_class,
                    original=original_term,
                    translations=translations,
                    **kwargs,
                )
            )

        return words_list

    def extract_row(self, row, word_class=None):
        kwargs = {}

        if word_class == 'nouns':
            original_term, translations, kwargs['gender'] = str(row[0]), row[2:], self.gender_mapper.get(row[1])
        else:
            original_term, translations = str(row[0]), row[1:]

        return original_term, translations, kwargs

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
