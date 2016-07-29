# -*- coding: utf-8 -*-

import numpy as np


# ---------------------------------------------------------------------------
# Função calculate_svd() - Calcula o SVD com a matriz palavra X musica e 
#                          retorna a posição espacial de cada musica
# - matrix: Matriz palavra X musica
# - k: tamanho do corte do SVD
# ---------------------------------------------------------------------------
def calculate_svd(matrix, k):
        U, sigma, V = np.linalg.svd(matrix, full_matrices=False)
        music_vectors = np.dot(np.diag(sigma), V[:,:k])
        return music_vectors
