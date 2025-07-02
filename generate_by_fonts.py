from image_creator import image_creator
from data_provider import data_provider

fonts_array = [
    "cyrillic Cancellaresca Script LET.ttf",
    "cyrillic_Kobzar KS.ttf",
    "cyrillic_Larisa script.ttf",
    "cyrillic_Script Thin Pen.ttf",
    "cyrillic_propisi.ttf",
]
font_size = 24
margin = 3
background_color = (255, 255, 255)  # белый
text_color = (0, 0, 0)  # черный

config = {
    "file_path": "text.txt",
    "fields": [
        "firstName",
        "lastName",
        "surname",
    ],
}

train_data, test_data = data_provider("files", config)

train_folder = "second_data_plast/train/images"
test_folder = "second_data_plast/test/images"

train_iterator = 0
test_iterator = 0

for font in fonts_array:
    image_creator_instance = image_creator()
    image_creator_instance.load_font(font, font_size)

    for index, word in enumerate(train_data):
        image_path, text = image_creator_instance.create_image(
            word, background_color, text_color, margin, train_iterator, train_folder
        )

        with open(f"{train_folder}/labels.txt", "a", encoding="utf-8") as file:
            file.write(f"{image_path}\t{text}" + "\n")

        train_iterator = train_iterator + 1

    for index, word in enumerate(test_data):
        image_path, text = image_creator_instance.create_image(
            word, background_color, text_color, margin, test_iterator, test_folder
        )

        with open(f"{test_folder}/labels.txt", "a", encoding="utf-8") as file:
            file.write(f"{image_path}\t{text}" + "\n")

        test_iterator = test_iterator + 1
