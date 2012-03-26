# test_ml.py
# For adaboost.py and entropy.py
# Example use of adaboost.py and entropy.py

# !/usr/bin/python 

import numpy as np

import entropy
import adaboost


# these should be 1 if the data point's rmse is lower (by some arbitrary amount) than the baseline rmse and 0 if not
entropy_labels = np.array([1, 1, 0, 0, 1, 0, 1, 0, 0, 1])

# these should be 1 if the data point's rmse is lower and -1 if not
adaboost_labels = np.array([1, 1, -1, -1, 1, -1, 1, -1, -1, 1])

# this is for maxent
# row represents a data point from an experiment
# each column represents a condition
# element (i, j) is 1 if condition j was true during data point i's experiment and 0 if not
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

# this is for boosting
# element (i, j) is 1 if condition j was true during data point i's experiment and -1 if not
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

# these give the indices of the top conditions (default is half as many results as there are conditions, rounded up)
# note that maxent doesn't care if the correlation is positive or negative; the top conditions may negatively effect the rmse
entropy_features = entropy.choose_features(data, entropy_labels)
print entropy_features
adaboost_features = adaboost.boost(predictions, adaboost_labels)
print adaboost_features
