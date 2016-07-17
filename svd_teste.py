import numpy as np
import fileinput
#from sklearn.cluster import KMeans


def calculate_svd(matrix):
    U, sigma, V = np.linalg.svd(matrix, full_matrices=False)
    print np.diag(sigma)
    print V
    print U
    import pdb;pdb.set_trace()
    X_a = np.dot(np.dot(U, np.diag(sigma)), np.transpose(V))
    return X_a

matrix = [[1,0,1,0,0],
[1,1,0,0,0],
[0,1,0,0,0],
[0,1,1,0,0],
[0,0,0,1,0],
[0,0,1,1,0],
[0,0,0,1,0],
[0,0,0,1,1]]

calculate_svd(matrix)

