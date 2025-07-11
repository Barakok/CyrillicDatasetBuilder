import random


def generate_passport_lines(config):
    train_data = []
    test_data = []

    for field in config["fields"]:
        file_name = "textData/" + field + ".txt"

        with open(file_name, "r", encoding="utf-8") as f:
            content = [line.strip() for line in f.read().split("\n")]

            array_len = len(content)
            split_index = int(array_len * 0.8)

            train_data.extend(content[:split_index])
            test_data.extend(content[split_index:])

    return train_data, test_data
