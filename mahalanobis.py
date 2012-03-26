# mahalanobis.py
# Detect outliers
# Test: mahalanobis.py [name of csv file]

# !/usr/bin/python

import numpy as np
from numpy import linalg as la

import math
import sys

import util


# x, y: lists of variables st. elements  with the same index belong to the same observation
def calculate_mahalanobis(x, y):
    covariance = np.cov(np.array([x, y]))

    mean = (sum(x) / len(x), sum(y) / len(y))
    xdiff = [xi - mean[0] for xi in x]
    ydiff = [eta - mean[1] for eta in y]
    diff = np.transpose(np.array([xdiff, ydiff]))

    dm = []
    for i in range(len(x)):
        dm.append(math.sqrt(np.dot(np.dot(diff[i], la.inv(covariance)), np.transpose(diff[i]))))
    return dm


# remove from x and y elements with high mahalanobis distance
def remove_outliers(x, y):
    dm = calculate_mahalanobis(x, y)
    threshold = 2 * sum(dm) / len(dm) # is this the best value?

    new_x, new_y, removed = [], [], []
    for i in range(len(dm)):
        if dm[i] <= threshold:
            new_x.append(x[i])
            new_y.append(y[i])
            removed.append(i)
    return (new_x, new_y, removed)


def main(filename):
    x, y = util.process_csv_list(filename)
    dm = calculate_mahalanobis(x, y)
    dm.sort()
    print dm
    

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
