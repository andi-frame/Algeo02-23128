from image_processing import turn_grayscale
from image_processing import resize_image
import numpy as np

def data_centering(image_paths):
    dataset = np.array([resize_image(turn_grayscale(image_path)) for image_path in image_paths])
    N, m, n = dataset.shape

    myu = np.zeros((m, n), dtype=float)
    for row in range(m):
        for col in range(n):
            sum_pixel = 0
            for i in range(N):
                sum_pixel += dataset[i, row, col]
            myu[row, col] = sum_pixel / N

    standardized = np.zeros_like(dataset, dtype=float)
    for i in range(N):
        for row in range(m):
            for col in range(n):
                standardized[i, row, col] = dataset[i, row, col] - myu[row, col]

    return myu, standardized