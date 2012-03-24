# mahalanobis.py
# Detect outliers

# !/usr/bin/python

import numpy as np
from numpy import linalg as la

import math
import re
import sys


# actual,data,t/f
csv_pat = re.compile("(\d[\d]?),([\d]?),[a-zA-Z]+")


# Returns array of data points from csv_list
def process_csv_list(csv_list):
    x, y = [], []
    for csv in csv_list:
        match = re.match(csv_pat, csv)
        if match:
            x.append((float)(match.group(1)))
            y.append((float)(match.group(2)))
    return (x, y)


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


def main(filename):

    file = open(filename)
    csv_list  = []
    for line in file.readlines():
        csv_list.append(line.strip())       
    file.close()

    x, y = process_csv_list(csv_list)
    dm = calculate_mahalanobis(x, y)
    print dm
    

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
