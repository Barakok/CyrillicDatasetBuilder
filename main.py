from image_creator import image_creator


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


with open("text.txt", "r", encoding="utf-8") as file:
    content = file.read()

content = content.strip()
words = content.split()

for index, word in enumerate(words):
    image_path, text = image_creator_instance.create_image(
        word, background_color, text_color, margin, index
    )

    with open("labels.txt", "a", encoding="utf-8") as file:
        file.write(f"{image_path}\t{text}" + "\n")
