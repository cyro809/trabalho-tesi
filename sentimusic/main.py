from tfidf.tfidf_matrix import generate_matrix
from music_svd import MusicSVD
from kmeans import KMeans



filename = 'database_min.json'
initial_matrix, vocabulary, music_list = generate_matrix(filename)

music_svd = MusicSVD()
music_svd.set_music_dict(music_list)

svd_matrix = music_svd.calculate_svd(initial_matrix, 4)
import pdb; pdb.set_trace()

# kmeans = KMeans(music_svd.music_list, svd_matrix, music_svd.music_dict)

# kmeans.execute_kfold_training()