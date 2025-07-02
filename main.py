from image_creator import image_creator
from data_provider import data_provider

# Входное слово
text = "Привет"

# Цвета
background_color = (255, 255, 255)  # белый
text_color = (0, 0, 0)  # черный

# Путь к TTF-файлу с рукописным шрифтом
font_path = "cyrillic_propisi.ttf"  # Замените на путь к вашему .ttf


# Размер шрифта
font_size = 24

margin = 3

image_creator_instance = image_creator()
image_creator_instance.load_font(font_path, font_size)

config = {
    "file_path": "text.txt",
    "fields": [
        "firstName",
        "lastName",
        "surname",
    ],
}

train_data, test_data = data_provider("files", config)

train_folder = "images/train"
test_folder = "images/test"

for index, word in enumerate(train_data):
    image_path, text = image_creator_instance.create_image(
        word, background_color, text_color, margin, index, train_folder
    )

    with open(f"{train_folder}/labels.txt", "a", encoding="utf-8") as file:
        file.write(f"{image_path}\t{text}" + "\n")

for index, word in enumerate(test_data):
    image_path, text = image_creator_instance.create_image(
        word, background_color, text_color, margin, index, test_folder
    )

    with open(f"{train_folder}/labels.txt", "a", encoding="utf-8") as file:
        file.write(f"{image_path}\t{text}" + "\n")
