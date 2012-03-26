# rmse.py
# Calculate error for experiments
# Test: rmse.py [name of csv file]

# !/usr/bin/python

import math
import sys

import util


def get_single_rmse(actual_val, data_val):
    return math.fabs(1 + (float)(actual_val) * 2/5 - (float)(data_val))


def calculate_rmse(actual, data):
    err_list = []
    for i in range(len(actual)):
        err_list.append(get_single_rmse(actual[i], data[i]))

    avg_err = sum(err_list) / len(err_list)
    
    sq_list = [x**2 for x in err_list]
    std_err = math.sqrt(sum(sq_list) / len(sq_list))

    return (avg_err, std_err)


def main(filename):
    actual, data = util.process_csv_list(filename)
    print "average error: %f \nstandard error: %f" % (calculate_rmse(actual, data))
    

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
