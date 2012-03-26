# adaboost.py

# !/usr/bin/python 

import numpy as np

import math
   

# labels: nx1 array; 1 if example is instance of improvement, -1 if not
# predictions: nxm array; 1 if feature m was active for example n, -1 if not
# T: number of rounds (ie, number of features to be chosen)
# returns features: 1xT array of chosen feature indices
def boost(labels, predictions, T=0):
    
    n = labels.size
    m = predictions.shape[1]
    if T == 0:
        T = m / 2

    features = np.zeros((1, T))

    alpha = np.zeros((1, T), Float)

    # error matrix: 1 if feature m made a mistake on input n, 0 else
    errors = np.zeros((n, m))
    for i in range(n):
        errors[i,:] = labels[i] * predictions[i,:]

    # reusable storage
    temp = np.zeros((1, T))

    # initialize distribution over examples
    D = np.ones((n, 1))
    D = D / D.sum()

    for t in range(T):
        
        # choose the best feature
        for i in range(m):
            temp[i] = (D * (errors[:,j] < 0)).sum()
        err, features[t] = temp.min(), temp.argmin()

        # update alpha and D
        alpha[t] = 0.5 * math.log((1 - err) / err)
        the_exp = exp(-(alpha[t]) * errors[:,features[t]])
        D = D * the_exp
        D = D / D.sum()

    return features
        
        
