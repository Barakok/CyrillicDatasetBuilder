import numpy as np
import random
from PIL import Image, ImageFilter


def jitter_image_soft(img, intensity=1):
    """
    Безопасный мягкий jitter: небольшие блочные смещения без ошибок границ.
    """
    img_np = np.array(img)
    h, w = img_np.shape[:2]
    jittered = np.copy(img_np)

    block_size = 10

    for y in range(0, h, block_size):
        for x in range(0, w, block_size):
            dx = random.randint(-intensity, intensity)
            dy = random.randint(-intensity, intensity)

            # Размер блока
            bh = min(block_size, h - y)
            bw = min(block_size, w - x)

            # Исходные координаты блока
            y_orig1, y_orig2 = y, y + bh
            x_orig1, x_orig2 = x, x + bw

            # Смещённые координаты
            y1 = min(max(0, y + dy), h - bh)
            x1 = min(max(0, x + dx), w - bw)
            y2, x2 = y1 + bh, x1 + bw

            # Копирование
            jittered[y_orig1:y_orig2, x_orig1:x_orig2] = img_np[y1:y2, x1:x2]

    img_jittered = Image.fromarray(jittered).filter(
        ImageFilter.GaussianBlur(radius=0.3)
    )
    return img_jittered
