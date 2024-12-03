from PIL import Image
import numpy as np
import os

def turn_grayscale(image_path):
    img = Image.open(image_path)

    img_array = np.array(img)

    if img_array.ndim == 3:  
        R = img_array[:, :, 0]
        G = img_array[:, :, 1]
        B = img_array[:, :, 2]

        grayscale = 0.2989 * R + 0.5870 * G + 0.1140 * B
    else:
        grayscale = img_array

    grayscale = grayscale.astype(np.float32)

    return grayscale


def resize_image(image_array):
    original_height, original_width = image_array.shape
    output_height, output_width = (10, 10)

    row_ratio = original_height / output_height
    col_ratio = original_width / output_width

    resized_image = np.zeros((output_height, output_width), dtype=image_array.dtype)

    for i in range(output_height):
        for j in range(output_width):
            ori_X = int(j * col_ratio)
            ori_Y = int(i * row_ratio)
            resized_image[i, j] = image_array[ori_Y, ori_X]

    return resized_image


def turn_to_1D(image_array):
    result = []
    for row in image_array:
        for pixel in row:
            result.append(pixel)
    return result


