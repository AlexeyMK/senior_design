# test_ml.py
# For adaboost.py and entropy.py

# !/usr/bin/python 

import numpy as np

import entropy
import adaboost


entropy_labels = np.array([1, 1, 0, 0, 1, 0, 1, 0, 0, 1])
adaboost_labels = np.array([1, 1, -1, -1, 1, -1, 1, -1, -1, 1])

data = np.array([[1, 1, 0, 1, 0], 
                 [1, 1, 0, 1, 0],
                 [0, 1, 0, 1, 1],
                 [0, 0, 0, 1, 1],
                 [1, 1, 0, 1, 0],
                 [0, 0, 0, 1, 1],
                 [1, 1, 0, 1, 0],
                 [0, 0, 0, 1, 1],
                 [0, 0, 0, 1, 1],
                 [0, 1, 1, 0, 0]])

predictions = np.array([[1, 1, -1, 1, -1], 
                        [1, 1, -1, 1, -1],
                        [-1, 1, -1, 1, 1],
                        [-1, -1, -1, 1, 1],
                        [1, 1, -1, 1, -1],
                        [-1, -1, -1, 1, 1],
                        [1, 1, -1, 1, -1],
                        [-1, -1, -1, 1, 1],
                        [-1, -1, -1, 1, 1],
                        [-1, 1, -1, 1, -1]])


entropy_features = entropy.choose_features(data, entropy_labels)
print entropy_features
adaboost_features = adaboost.boost(predictions, adaboost_labels)
print adaboost_features
