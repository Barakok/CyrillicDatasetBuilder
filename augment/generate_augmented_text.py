from PIL import ImageFont, ImageDraw, Image
from skew import skew_image
from baseline import wave_baseline
from shift import shift_image
from jitter import jitter_image_soft


def generate_augmented_text(text, font_path, font_size=48):
    font = ImageFont.truetype(font_path, font_size)
    dummy_img = Image.new("L", (1000, 100), 0)
    draw = ImageDraw.Draw(dummy_img)
    draw.text((10, 10), text, fill=255, font=font)
    cropped = dummy_img.crop(dummy_img.getbbox())

    img = skew_image(cropped)
    img = wave_baseline(img)
    img = shift_image(img)
    img = jitter_image_soft(img)

    return img


img = generate_augmented_text("Иванов", "cyrillic_propisi.ttf")
print("img", img)
img.save(f"aug_test_image.png")
