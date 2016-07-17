def build_k_fold(array, test_size):
    k_fold_training = []
    k_fold_test = []
    number_folds = len(array)/test_size

    for i in range(0,number_folds):
        fold_test = array[i*test_size:(i+1)*test_size]
        fold_training = [x for x in array if x not in fold_test]
        k_fold_test.append(fold_test)
        k_fold_training.append(fold_training)

    return (k_fold_training, k_fold_test)
    