from utils.get_words_from_file import get_words_from_file
from utils.generate_passport_lines import generate_passport_lines
from utils.generate_csv_lines import get_address_from_csv


def data_provider(mode, config):
    if mode == "file":
        return get_words_from_file(config)

    if mode == "files":
        return generate_passport_lines(config)

    if mode == "csv":
        return get_address_from_csv(config)
