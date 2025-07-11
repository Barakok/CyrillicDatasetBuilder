import numpy as np
from PIL import Image


def wave_baseline(img, amplitude=5, period=80):
    img_np = np.array(img)
    h, w = img_np.shape[:2]
    result = np.zeros_like(img_np)

    for x in range(w):
        offset = int(amplitude * np.sin(2 * np.pi * x / period))
        if img_np.ndim == 2:  # grayscale
            result[:, x] = np.roll(img_np[:, x], offset)
        else:  # RGB or RGBA
            result[:, x, :] = np.roll(img_np[:, x, :], offset)

    return Image.fromarray(result)
