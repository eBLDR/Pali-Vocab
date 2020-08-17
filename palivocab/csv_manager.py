import csv

from palivocab import config


class CSVManager:
    type_mapper = {
        'verbs': config.VERBS_FILE_PATH,
        'nouns': config.NOUNS_FILE_PATH,
        'indeclinables': config.INDECLINABLES_FILE_PATH,
    }

    def get_data_set(self, word_class):
        if word_class not in self.type_mapper.keys():
            raise NotImplementedError

        return self.prepare_data_set(
            self.load_csv(self.type_mapper[word_class]),
        )

    @staticmethod
    def load_csv(filename):
        with open(filename, 'r') as csv_file:
            raw_data = [
                row for row in csv.reader(csv_file)
            ]

        return raw_data

    @staticmethod
    def prepare_data_set(raw_data):
        data_set = {}

        for row in raw_data:
            pali_term, english_term = str(row[0]), row[1:]

            if pali_term in data_set:
                continue

            data_set[pali_term] = english_term

        return data_set
