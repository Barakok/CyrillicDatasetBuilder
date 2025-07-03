import pandas as pd


def get_address_from_csv(config):
    df = pd.read_csv(config["file_path"])

    address_text_list = df["text"].tolist()

    array_len = len(address_text_list)
    split_index = int(array_len * 0.8)

    train_data = address_text_list[:split_index]
    test_data = address_text_list[split_index:]

    return train_data, test_data
