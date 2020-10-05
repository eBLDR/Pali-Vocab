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
            dict_like_data = [
                row for row in csv.DictReader(csv_file)
            ]

        return dict_like_data

    def prepare_data_set(self, dict_like_data, word_class=None):
        words_list = []

        for word_data in dict_like_data:
            original_term = word_data.pop('original')
            translations = word_data.pop('translation', []).split(';')

            if original_term in words_list:
                continue

            if 'gender' in word_data:
                word_data['gender'] = self.gender_mapper.get(word_data['gender'])

            words_list.append(
                Word.factory_from_word_class(
                    word_class=word_class,
                    original=original_term,
                    translations=translations,
                    **word_data,
                )
            )

        return words_list

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
