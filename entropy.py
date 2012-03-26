# entropy.py

# !/usr/bin/python 

import numpy as np
   

def multiply_p_logp(P):
    return min([0, P * np.log2(P)])


def calculate_entropy(P):
    return - (multiply_p_logp(P) + multiply_p_logp(1-P))


# data: nx1 array; corresponds to the slice of data for this feature
def calculate_conditional_entropy(data, labels, split_val):
    split_f = (data < split_val)
    px = split_f.mean()
    sum_y_given_x = (labels and split_f).sum()
    sum_y_given_notx = (labels and (not split_f)).sum()
    return px * calculate_entropy(sum_y_given_x / split_f.sum()) + (1 - px) * calculate_entropy(sum_y_given_notx / (not split_f).sum())


# data: nxd array; 1 if feature d was active for example n, -1 else
# labels: nx1 array; 1 if example n showed improvement, 0 else
# T: number of rounds (ie, number of features to be chosen)
# returns feature_idx: 1xT array of chosen feature indices
def choose_features(data, labels, T=0):

    n = labels.size
    d = data.shape[1]
    if T = 0:
        T = d / 2

    # calculate entropy of label distribution
    H = calculate_entropy(labels)

    ig = np.zeros((d, 1), Float)
    split_val = 0 # since the features are binary, the split value is known

    for i in range(d):
        
        # check for constants
        temp = data[:,i].sum() 
        if temp == 0 or temp == n:
            ig[i] = 0

        ig[i] = H - calculate_conditional_entropy(data[,i], labels, split_val)
        
    
    return np.argsort(ig)[d-T+1:]
