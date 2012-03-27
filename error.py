# error.py
# Usage: error.py [name of csv file]

# !/usr/bin/python

import os
import sys

import mahalanobis
import rmse
import util

# TODO: add support for removing all data points from users who produce outliers
def main(dirname):    

    filenames = os.listdir(dirname)
    for filename in filenames:
        if not ".json" in filename:
            continue

        filename = filename[:-5] + ".csv"
        print "Processing %s... " % filename[:-4],
        x, y, ids = util.process_csv_list(os.path.join(dirname, filename))
        new_x, new_y, removed = mahalanobis.remove_outliers(x, y) 
        print "done"
        print "Removed %d outlying point(s)" % (len(x) - len(new_x))
        print "Average error: %f, standard error: %f" % (rmse.calculate_rmse(new_x, new_y))
        print
    

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
