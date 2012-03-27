# ml.py
# To call: python ml.py (name of directory of experiment results)

# !/usr/bin/python 

import numpy as np

import os
import sys

import adaboost
import entropy
import mahalanobis
import rmse
import util


def make_arrays(dirname):
    data, predictions, boost_labels, maxent_labels = [], [], [], []
   
    filenames = os.listdir(dirname)
    for filename in filenames:
        if not ".json" in filename:
            continue

        conditions = util.process_json(os.path.join(dirname, filename))
    
        x, y, idx = util.process_csv_list(os.path.join(dirname, filename[:-5] + ".csv"))
        for i in range(len(x)):
            tempd, tempp = [0] * (util.num_conditions + 1), [0] * (util.num_conditions + 1)
            for j in conditions:
                tempd[j] = 1
                tempp[j] = -1
            data.append(tempd)
            predictions.append(tempp)

            error = rmse.get_single_rmse(x[i], y[i])
            if error <= util.base_error / 2:
                boost_labels.append(1)
                maxent_labels.append(1)
            else:
                boost_labels.append(-1)
                maxent_labels.append(0)

    data = np.array(data)
    predictions = np.array(predictions)
    boost_labels = np.array(boost_labels)
    maxent_labels = np.array(maxent_labels)
    return (data, predictions, boost_labels, maxent_labels)


def main(dirname):
    data, predictions, boost_labels, maxent_labels = make_arrays(dirname)

    boost_features = adaboost.boost(predictions, boost_labels)
    maxent_features = entropy.choose_features(data, maxent_labels)

    condition_dict = dict((v, k) for k, v in util.conditions.iteritems())
    features = [condition_dict[x] for x in boost_features if x in maxent_features]
    print "Most predictive feature(s):"
    for feature in features:
        print feature
    


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
