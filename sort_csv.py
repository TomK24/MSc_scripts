#!/usr/bin/python

#########################################################
# Created by Thomas Kenyon, 2020

#This script reorders the  unordered data in a csv file containing my docking H bond occupancy data. From largest to smallest
#########################################################

import os
import sys
import re


def count(l): # sums all numbers in a line of csv data
    l2 = l.strip()
    lsplit = l2.split(",")[1:]
    tot = 0.0
    for i in lsplit:
        if True:
            new = float(i)
            tot += new
    return tot

csvl = []
file = open("hbond.csv", "r")
csvl = file.readlines()
file.close()
csv = csvl[1:]

n = len(csv) 

# Traverse through all array elements 
for i in range(n): 

    # Last i elements are already in place 
    for j in range(0, n-i-1): 

        # traverse the array from 0 to n-i-1 
        # Swap if the element found is greater 
        # than the next element 
        if count(csv[j]) > count(csv[j+1]) : 
            csv[j], csv[j+1] = csv[j+1], csv[j] 
csv.reverse()
sorted_csv = [csvl[0]] + csv
# for i in sorted_csv:
#     print(count(i))
new_file = open("output_sorted.csv", "w")
new_file.writelines(sorted_csv)
new_file.close()


print("All done!!")



        
