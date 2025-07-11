from PIL import Image
import random


def shift_image(img, max_shift=5):
    x_shift = random.randint(-max_shift, max_shift)
    y_shift = random.randint(-max_shift, max_shift)
    return img.transform(
        img.size, Image.AFFINE, (1, 0, x_shift, 0, 1, y_shift), resample=Image.BICUBIC
    )
