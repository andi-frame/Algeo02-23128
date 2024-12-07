from PIL import Image
import numpy as np
import os

def turn_grayscale(image_path):
    img = Image.open(image_path).convert("L") 
    grayscale = np.array(img, dtype=np.float32)  
    return grayscale

def resize_image(image_array, output_height=10, output_width=10):
    img = Image.fromarray(image_array)
    img_resized = img.resize((output_width, output_height), Image.ANTIALIAS) 
    resized_array = np.array(img_resized, dtype=image_array.dtype)
    return resized_array

def turn_to_1D(image_array):
    return image_array.flatten()

def data_centering(image_paths):
    dataset = np.array([resize_image(turn_grayscale(image_path)) for image_path in image_paths])
    N, m, n = dataset.shape

    myu = np.mean(dataset, axis=0)

    standardized = dataset - myu
    return myu, standardized.reshape(N, -1) 

def singular_value_decomposition(standardized_data, num_components=1):
    U, S, Vt = np.linalg.svd(standardized_data, full_matrices=False)
    Uk = Vt[:num_components].T  
    Z = np.dot(standardized_data, Uk)  
    return Z, Uk, S[:num_components]

def query_projection(query_image_path, myu, Uk):
    query_grayscale = turn_grayscale(query_image_path)
    query_resized = resize_image(query_grayscale)
    query_flattened = turn_to_1D(query_resized)

    q_centered = query_flattened - myu.flatten()
    q_projected = np.dot(q_centered, Uk)
    return q_projected

def compute_euclidean_distance(query_projection, dataset_projections):
    distances = np.linalg.norm(dataset_projections - query_projection, axis=1)  
    return distances

def find_most_similar(query_image_path, myu, Uk, dataset_projections, top_k=5):
    query_proj = query_projection(query_image_path, myu, Uk)
    distances = compute_euclidean_distance(query_proj, dataset_projections)

    sorted_indices = np.argsort(distances) 
    return sorted_indices[:top_k], distances[sorted_indices[:top_k]]
