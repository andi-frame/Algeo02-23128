from PIL import Image
import numpy as np
import io
import os


def image_to_blob(image_path):
    image = Image.open(image_path)

    img_byte_arr = io.BytesIO()

    image.save(img_byte_arr, format="PNG")

    img_byte_arr = img_byte_arr.getvalue()
    
    return img_byte_arr

# Fungsi untuk mengonversi gambar menjadi grayscale
def turn_grayscale(image_blob):
    img = Image.open(io.BytesIO(image_blob)).convert("L")  
    grayscale = np.array(img, dtype=np.float32)  
    return grayscale

# Fungsi untuk meresize gambar ke ukuran tertentu
def resize_image(image_array, output_height=20, output_width=20):  
    img = Image.fromarray(image_array)
    img_resized = img.resize((output_width, output_height), Image.Resampling.LANCZOS)  # Resize gambar
    resized_array = np.array(img_resized, dtype=image_array.dtype)  # Kembalikan ke array numpy
    return resized_array

# Fungsi untuk mengubah gambar menjadi vektor 1D
def turn_to_1D(image_array):
    return image_array.flatten()

# Fungsi untuk menghilangkan rata-rata (data centering)
def data_centering(image_paths):
    dataset = np.array([resize_image(turn_grayscale(image_path)) for image_path in image_paths])
    N, m, n = dataset.shape  # Dapatkan dimensi dataset

    myu = np.mean(dataset, axis=0)  # Hitung rata-rata gambar

    standardized = dataset - myu  # Centering data (mengurangi rata-rata)
    return myu, standardized.reshape(N, -1)  # Kembalikan dataset yang sudah distandarisasi dalam bentuk 1D

# Fungsi Singular Value Decomposition (SVD) untuk reduksi dimensi
def singular_value_decomposition(standardized_data, num_components=5):  
    U, S, Vt = np.linalg.svd(standardized_data, full_matrices=False)  # SVD pada data standar
    Uk = Vt[:num_components].T  # Ambil komponen utama (PCA)
    Z = np.dot(standardized_data, Uk)  # Proyeksikan data ke dalam ruang komponen utama
    return Z, Uk, S[:num_components]  # Kembalikan proyeksi data dan komponen utama

# Fungsi untuk memproyeksikan gambar query ke dalam ruang komponen utama
def query_projection(query_image_path, myu, Uk):
    query_grayscale = turn_grayscale(query_image_path)
    query_resized = resize_image(query_grayscale)
    query_flattened = turn_to_1D(query_resized)

    q_centered = query_flattened - myu.flatten()  # Centering gambar query dengan rata-rata dataset
    q_projected = np.dot(q_centered, Uk)  # Proyeksikan gambar query ke ruang komponen utama
    return q_projected

# Fungsi untuk menghitung jarak Euclidean antara gambar query dan dataset
def compute_euclidean_distance(query_projection, dataset_projections):
    distances = np.linalg.norm(dataset_projections - query_projection, axis=1)  # Hitung Euclidean Distance
    return distances

# Fungsi untuk menemukan gambar yang paling mirip dengan gambar query
def find_most_similar(query_image_path, myu, Uk, dataset_projections, top_k=5):
    query_proj = query_projection(query_image_path, myu, Uk)  # Proyeksikan gambar query
    distances = compute_euclidean_distance(query_proj, dataset_projections)  # Hitung jarak Euclidean

    sorted_indices = np.argsort(distances)  # Urutkan berdasarkan jarak terkecil
    return sorted_indices[:top_k], distances[sorted_indices[:top_k]]  # Kembalikan indeks dan jarak gambar paling mirip
