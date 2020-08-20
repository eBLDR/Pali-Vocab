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

    def get_data_set(self, source, word_class):
        file_path = self.generate_file_path(source, word_class)

        return self.prepare_data_set(
            self.load_csv(file_path),
        )

    def generate_file_path(self, source, word_class):
        file_path = os.path.join(
            config.SRC_PATH,
            source.lower(),
            self.word_class_file_name_mapper.get(word_class, ''),
        )

        if not os.path.isfile(file_path):
            raise FileNotFoundError

        return file_path

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
