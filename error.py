# error.py
# Usage: error.py [name of csv file]

# !/usr/bin/python

import sys

import mahalanobis
import rmse
import util


def main(filename):    
    x, y = util.process_csv_list(filename)
    new_x, new_y = mahalanobis.remove_outliers(x, y)
    print "removed %d outlying point(s)" % (len(x) - len(new_x))
    print "average error: %f \nstandard error: %f" % (rmse.calculate_rmse(new_x, new_y))
    

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
