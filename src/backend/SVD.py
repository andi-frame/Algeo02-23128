from data_centering import data_centering
import numpy as np

def singular_value_decomposition(standardized_data, num_components):
    N, M = standardized_data.shape
    C = np.zeros((M, M))  
    for i in range(M):
        for j in range(M):
            sum_cov = 0
            for k in range(N):
                sum_cov += standardized_data[k, i] * standardized_data[k, j]
            C[i, j] = sum_cov / N

    def power_iteration(A, num_iter=100, tol=1e-6):
        n = A.shape[0]
        b_k = np.random.rand(n)
        b_k = b_k / np.linalg.norm(b_k)

        for _ in range(num_iter):
            b_k1 = np.dot(A, b_k)
            b_k1_norm = np.linalg.norm(b_k1)
            b_k1 = b_k1 / b_k1_norm

            if np.linalg.norm(b_k1 - b_k) < tol:
                break

            b_k = b_k1

        eigenvalue = np.dot(b_k.T, np.dot(A, b_k))
        eigenvector = b_k

        return eigenvalue, eigenvector

    eigenvalues = []
    eigenvectors = []
    for _ in range(num_components):
        eigenvalue, eigenvector = power_iteration(C)

        eigenvalues.append(eigenvalue)
        eigenvectors.append(eigenvector)

        C -= eigenvalue * np.outer(eigenvector, eigenvector)

    eigenvalues = np.array(eigenvalues)
    U_k = np.array(eigenvectors).T  

    Z = np.zeros((N, num_components))
    for i in range(N):
        for j in range(num_components):
            for k in range(M):
                Z[i, j] += standardized_data[i, k] * U_k[k, j]

    return Z, U_k, eigenvalues