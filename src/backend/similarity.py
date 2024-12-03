import numpy as np
from image_processing import turn_grayscale, resize_image, turn_to_1D

def query_projection(query_image_path, myu, Uk):
    query_grayscale = turn_grayscale(query_image_path)
    query_resized = resize_image(query_grayscale)
    query_flattened = turn_to_1D(query_resized)

    q_centered = query_flattened - myu.flatten()
    q_projected = np.dot(q_centered, Uk)

    return q_projected

def compute_euclidean_distance(query_projection, dataset_projections):
    distances = []
    for zi in dataset_projections:
        distance = np.sqrt(np.sum((query_projection - zi) ** 2))
        distances.append(distance)
    return distances

def find_most_similar(query_image_path, myu, Uk, dataset_projections, top_k=5):
    query_projection = query_projection(query_image_path, myu, Uk)
    distances = compute_euclidean_distance(query_projection, dataset_projections)

    sorted_indices = np.argsort(distances)
    return sorted_indices[:top_k], np.array(distances)[sorted_indices[:top_k]]
