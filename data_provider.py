from get_words_from_file import get_words_from_file
from generate_passport_lines import generate_passport_lines


def data_provider(mode, config):
    if mode == "file":
        return get_words_from_file(config)

    if mode == "files":
        return generate_passport_lines(config)
