from PIL import Image, ImageDraw, ImageFont


class image_creator:
    def __init__(self, background_color, margin):
        self.background_color = background_color
        self.margin = margin

    def load_font(self, font_path, font_size):
        self.font_path = font_path
        # Загружаем шрифт
        self.font = ImageFont.truetype(font_path, font_size)

    def set_fonts(self, fonts_combinations):
        self.fonts = {}

        for key in fonts_combinations:
            self.fonts[key] = ImageFont.truetype(
                fonts_combinations[key]["font"], fonts_combinations[key]["size"]
            )

    def create_image(self, text, text_color, font, index, image_folder):
        # Создаем временное изображение для измерения размера текста
        tmp_img = Image.new("RGB", (1, 1))
        draw = ImageDraw.Draw(tmp_img)

        bbox = draw.textbbox((0, 0), text, font=self.fonts[font])
        text_width = bbox[2] - bbox[0] + self.margin
        text_height = bbox[3] - bbox[1] + self.margin

        # Создаем изображение с нужными размерами
        image = Image.new("RGB", (text_width, text_height), self.background_color)
        draw = ImageDraw.Draw(image)

        # Рисуем текст
        draw.text((-bbox[0], -bbox[1]), text, font=self.fonts[font], fill=text_color)

        image_path = f"output_{index}.png"

        # Сохраняем изображение
        image.save(f"{image_folder}/{image_path}")

        return image_path, text
