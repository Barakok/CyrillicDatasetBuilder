def get_words_from_file(config):
    with open(config["file_path"], "r", encoding="utf-8") as file:
        words = file.read().strip().split("\n")

    array_len = len(words)
    split_index = int(array_len * 0.8)

    train_data = words[:split_index]
    test_data = words[split_index:]

    return train_data, test_data
