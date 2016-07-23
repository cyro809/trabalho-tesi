from tfidf.tfidf_matrix import generate_matrix
from music_svd import calculate_svd
from kmeans import KMeans



filename = 'database_min.json'
initial_matrix, vocabulary, music_list, music_dict = generate_matrix(filename)

svd_matrix = calculate_svd(initial_matrix, 4)

kmeans = KMeans(music_list, svd_matrix, music_dict)

kmeans.execute_kfold_training()