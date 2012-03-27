# util.py

# !/usr/bin/python

import re


# from base_case_2
base_error = 0.95833


# actual,data,t/f
csv_pat = re.compile("(\d[\d]?),([\d]?),[a-zA-Z]+,([\w]+)")


# Returns lists of data points from the csv file
def process_csv_list(filename):
    f = open(filename)
    csv_list  = []
    for line in f.readlines():
        csv_list.append(line.strip())       
    f.close()

    x, y, ids = [], [], []
    for csv in csv_list:
        match = re.match(csv_pat, csv)
        if match and len(match.group(2)) > 0: # get rid of ones with no review
            x.append((float)(match.group(1)))
            y.append((float)(match.group(2)))
            ids.append(match.group(3))
    return (x, y, ids)


num_conditions = 7


# Features
conditions = {("thank_on_bad_review", "true"):0, 
              ("review_will_be_anonymous", "anonymous"):1, 
              ("review_will_be_anonymous", "public"):2,
              ("why_leave_a_review", "personal_gain"):3,
              ("why_leave_a_review", "collective_gain"):4,
              ("why_leave_a_review", "experimental_validity"):5,
              ("review_is_mandatory", "true"):6,
              ("show_earned_so_far", "true"):7}


# "condition_name": bool OR "value_name"
json_pat = re.compile("\"([a-z_]+)\": [\"]?([a-z_]+)[\"]?,?")


# Returns list of features from the json file
def process_json(filename):
    f = open(filename)
    line = f.readline()
    f.close()

    conditions_found = []
    groups = re.findall(json_pat, line)
    for condition, value in groups:
        if (condition, value) in conditions:
            conditions_found.append(conditions[(condition, value)])
    return conditions_found
