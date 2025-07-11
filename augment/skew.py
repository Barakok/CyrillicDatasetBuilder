from PIL import Image
import random


def skew_image(img, max_skew=25):
    w, h = img.size
    skew_deg = random.uniform(-max_skew, max_skew)
    skew_rad = skew_deg * 3.14 / 180

    xshift = abs(skew_rad) * h
    new_width = int(w + xshift)

    return img.transform(
        (new_width, h),
        Image.AFFINE,
        (1, skew_rad, -xshift if skew_deg > 0 else 0, 0, 1, 0),
        resample=Image.BICUBIC,
    )
