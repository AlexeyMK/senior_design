# util.py

# !/usr/bin/python

import re


# actual,data,t/f
csv_pat = re.compile("(\d[\d]?),([\d]?),[a-zA-Z]+")


# Returns array of data points from csv_list
def process_csv_list(filename):
    file = open(filename)
    csv_list  = []
    for line in file.readlines():
        csv_list.append(line.strip())       
    file.close()

    x, y = [], []
    for csv in csv_list:
        match = re.match(csv_pat, csv)
        if match and len(match.group(2)) > 0: # get rid of ones with no review
            x.append((float)(match.group(1)))
            y.append((float)(match.group(2)))
    return (x, y)
