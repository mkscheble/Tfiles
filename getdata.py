import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import random
import pickle


def create_training_data(img_size, datadirs, categories):
    training_data = []
    for i in np.arange(len(datadirs)):
        count = 0
        directory = os.path.join(datadirs[i], categories[0])
        # print(directory)
        for img in os.listdir(directory):
            try:
                img_array = cv2.imread(os.path.join(directory, img), cv2.IMREAD_GRAYSCALE)
                print(np.shape(img_array))
                new_array = cv2.resize(img_array, (img_size, img_size))
                count += 1
                training_data.append([new_array, i])
                # print(count)
            except Exception as e:
                pass
    return training_data

def reshaper(training_data, img_size):
    x = []
    y = []
    for features, label in training_data:
        x.append(features)
        y.append(label)
    x = np.array(x).reshape(-1, img_size, img_size, 1)
    y = np.array(y)
    return x, y


def main():
    img_size = 50
    datadirs = [r"C:\Users\MarkScheble.Jr\Desktop\data_rbc\dataset_regular", r"C:\Users\MarkScheble.Jr\Desktop\data_rbc\dataset_spiky"]
    categories = ['train', 'test', 'validation']
    training_data = create_training_data(img_size, datadirs, categories)
    random.shuffle(training_data)
    random.shuffle(training_data)
    for sample in training_data[:10]:
        print(sample[1])
    x, y = reshaper(training_data, img_size)

    pickle_out = open("x.pickle", "wb")
    pickle.dump(x, pickle_out)
    pickle_out.close()

    pickle_out = open("y.pickle", "wb")
    pickle.dump(y, pickle_out)
    pickle_out.close()

    print("success")


if __name__ == "__main__":
    main()







