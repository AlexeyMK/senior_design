# entropy.py

# !/usr/bin/python 

import numpy as np
   

def multiply_p_logp(P):
    if P == 0: 
        return 0
    else:
        return P * np.log2(P)


def calculate_entropy(P):
    temp = multiply_p_logp(P) + multiply_p_logp(1-P)
    if temp == 0:
        return temp
    else:
        return - temp


# data: nx1 array; corresponds to the slice of data for this feature
def calculate_conditional_entropy(data, labels):
    px = data.mean()
    sum_y_given_x = (float)(np.logical_and(labels, data).sum())
    sum_y_given_notx = (float)(np.logical_and(labels, np.logical_not(data)).sum())
    return px * calculate_entropy(sum_y_given_x / data.sum()) + (1-px) * calculate_entropy(sum_y_given_notx / np.logical_not(data).sum())


# data: nxd array; 1 if feature d was active for example n, 0 else
# labels: nx1 array; 1 if example n showed improvement, 0 else
# T: number of rounds (ie, number of features to be chosen)
# returns feature_idx: 1xT array of chosen feature indices
def choose_features(data, labels, T=0):

    n = labels.size
    d = data.shape[1]
    if T == 0:
        T = (d + 2 - 1) / 2

    # calculate entropy of label distribution
    H = calculate_entropy(labels.mean())

    ig = np.zeros(d, float)

    for i in range(d):
        
        # check for constants
        temp = data[:,i].sum() 
        if temp == n or temp == 3*n:
            ig[i] = 0

        ig[i] = H - calculate_conditional_entropy(data[:,i], labels)
        
    return (np.argsort(ig.flatten())[d-T:])[::-1]
