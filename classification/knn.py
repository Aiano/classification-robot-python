import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

__data = []
__label = []
__data_array = None
__label_array = None
knn = None


def add_sample(feathers: list, labels: int):
    # feathers:
    # [[coordinate...],
    #   [area...],
    #   [aspect ratio...]]
    # labels: class of these feathers
    global __data, __label, __data_array, __label_array
    coordinates, areas, ars = feathers
    tmp_list = [labels]
    if not len(coordinates) == len(areas) == len(ars):
        print("Error occur in function add_sample : length error.")
        exit(1)
    for i in range(len(coordinates)):
        __data.append([areas[i], ars[i]])
        __label.append(tmp_list)


def train_data():
    global __data_array, __label_array, __data, __label, knn
    __data_array = np.array(__data).astype(np.float32)
    __label_array = np.array(__label).astype(np.float32)
    if __data_array is None or __label_array is None:
        print("Error occur in function train_data : __data_array or __label_array is empty.")
        exit(1)
    knn = cv.ml.KNearest_create()
    knn.train(__data_array, cv.ml.ROW_SAMPLE, __label_array)


def save_data(file: str):
    global knn
    if not knn.isTrained():
        print("Error occur in function save_data :knn hasn't been trained yet.")
        exit(1)
    knn.save(file)
    print("Saved successfully.")


def load_data(file: str):
    global knn
    knn = cv.ml.KNearest_load(file)
    if not knn.isTrained():
        print("Error occur in function load_data :Can't open the file.")
        exit(1)
    print("Loaded successfully.")


def predict(feathers: list) -> np.ndarray:
    global knn
    __test = [[feathers[1][i], feathers[2][i]] for i in range(len(feathers[0]))]
    __test_array = np.array(__test).astype(np.float32)
    ret, results, neighbours, dist = knn.findNearest(__test_array, 3)
    return results


def show_data_in_plt():
    plt.scatter(__data_array[:, 0], __data_array[:, 1], 80)
    plt.show()
