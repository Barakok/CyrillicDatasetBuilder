from PIL import Image, ImageDraw, ImageFont


class image_creator:
    def load_font(self, font_path, font_size):
        self.font_path = font_path
        # Загружаем шрифт
        self.font = ImageFont.truetype(font_path, font_size)

    def create_image(self, text, background_color, text_color, margin, index):
        # Создаем временное изображение для измерения размера текста
        tmp_img = Image.new("RGB", (1, 1))
        draw = ImageDraw.Draw(tmp_img)

        bbox = draw.textbbox((0, 0), text, font=self.font)
        text_width = bbox[2] - bbox[0] + margin
        text_height = bbox[3] - bbox[1] + margin

        # Создаем изображение с нужными размерами
        image = Image.new("RGB", (text_width, text_height), background_color)
        draw = ImageDraw.Draw(image)

        # Рисуем текст
        draw.text((-bbox[0], -bbox[1]), text, font=self.font, fill=text_color)

        image_path = f"output_{index}.png"

        # Сохраняем изображение
        image.save(f"images/{image_path}")

        print("Изображение сохранено как output.png")

        return image_path, text
