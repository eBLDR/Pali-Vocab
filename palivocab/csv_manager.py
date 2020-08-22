import csv
import os

from palivocab import config


class CSVManager:
    word_class_file_name_mapper = {
        'verbs': config.VERBS_FILENAME,
        'nouns': config.NOUNS_FILENAME,
        'indeclinables': config.INDECLINABLES_FILENAME,
        'pronouns': config.PRONOUNS_FILENAME,
    }

    def generate_path(self, source=None, lesson_number=None, word_class=None):
        path = os.path.join(
            config.SRC_PATH,
            source.lower() if source else '',
            self.generate_lesson_folder_name(lesson_number) if lesson_number else '',
            self.word_class_file_name_mapper.get(word_class, '') if word_class else '',
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
        return [
            file.replace('.csv', '') for file in os.listdir(
                self.generate_path(
                    source,
                    lesson_number=lesson_number,
                ),
            )
        ]

    def generate_data_set(self, source, lesson_number=None, word_class=None):
        data_set = {}

        if lesson_number == config.ALL_STRING:
            for lesson_number_ in self.get_available_lessons(source):
                data_set.update(
                    self.load_lesson(
                        source,
                        lesson_number=lesson_number_,
                        word_class=word_class,
                    )
                )
        else:
            data_set = self.load_lesson(
                source,
                lesson_number=lesson_number,
                word_class=word_class,
            )

        return data_set

    def load_lesson(self, source, lesson_number, word_class=None):
        lesson_data = {}

        if word_class == config.ALL_STRING:
            for word_class_ in self.get_available_word_classes(
                    source,
                    lesson_number=lesson_number,
            ):
                lesson_data.update(
                    self.load_word_class(
                        source,
                        lesson_number=lesson_number,
                        word_class=word_class_,
                    )
                )
        else:
            lesson_data = self.load_word_class(
                source,
                lesson_number=lesson_number,
                word_class=word_class,
            )

        return lesson_data

    def load_word_class(self, source, lesson_number=None, word_class=None):
        file_path = self.generate_path(
            source,
            lesson_number=lesson_number,
            word_class=word_class,
        )

        return self.prepare_data_set(
            self.load_csv(file_path),
        )

    @staticmethod
    def load_csv(filepath):
        with open(filepath, 'r') as csv_file:
            raw_data = [
                row for row in csv.reader(csv_file)
            ]

        return raw_data

    @staticmethod
    def prepare_data_set(raw_data):
        data_set = {}

        for row in raw_data:
            pali_term, english_terms = str(row[0]), row[1:]

            if pali_term in data_set:
                continue

            data_set[pali_term] = english_terms

        return data_set

    @staticmethod
    def generate_lesson_folder_name(lesson_number: int) -> str:
        lesson_string = str(lesson_number)

        if len(lesson_string) == 1:
            lesson_string = f'0{lesson_string}'

        return config.LESSON_FOLDER_NAME.format(
            two_digit_number=lesson_string,
        )
