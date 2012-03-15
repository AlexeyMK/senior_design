# rmse.py
# Calculate error for experiments

# !/usr/bin/python

import math
import re
import sys


# actual,data,t/f
csv_pat = re.compile("(\d[\d]?),([\d]?),[a-zA-Z]+")


def process_csv(csv_list):

    err_list = []
    for csv in csv_list:
        match = re.match(csv_pat, csv)
        if match: 
            if len(match.group(2)) == 0:
                err_list.append() # treat no review same as max err
            else:
                err_list.append(math.fabs(1+ (float)(match.group(1)) * 2/5 - (float)(match.group(2))))
        else:
            continue

    avg_err = sum(err_list) / len(err_list)
    
    sq_list = [x**2 for x in err_list]
    std_err = math.sqrt(sum(sq_list) / len(sq_list))

    return (avg_err, std_err)


def main(filename):

    file = open(filename)
    csv_list  = []
    for line in file.readlines():
        csv_list.append(line.strip())       
    file.close()

    print "average error: %f \nstandard error: %f" % (process_csv(csv_list))
    

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
