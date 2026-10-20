#!/usr/bin/python3

import argparse
import os
import re

def custom_sort(z, x):                   #<------------Sorting method, keeps calling find_lowest until length of sorted list = length of unsorted
    not_sorted = z
    names_not_sorted = x
    is_sorted = []
    names_is_sorted = []
    index_of_sorted = []              #<-----------find_lowest returns the index of lowest value it finds, index is added to this list
    # for i in range(len(not_sorted)):             so that the next time it is called it doesn't pick the same value.
    while not len(not_sorted) == len(is_sorted):
        next_lowest = find_lowest(not_sorted, index_of_sorted)
        is_sorted += [next_lowest[1]]
        index_of_sorted += [next_lowest[0]]
        names_is_sorted += [names_not_sorted[next_lowest[0]]] 
    # print("not sorted: " + str(not_sorted))
    # print("sorted: " + str(is_sorted))
    # print(index_of_sorted)
    return [is_sorted, names_is_sorted]

def find_lowest(a,b):   #<------part of my sort method. Finds smallest value in list a with an index that isn't already in list b. returns the value and the index??
    not_sorted2 = a
    # is_sorted = []
    to_return = []
    index_of_sorted2 = b
    min = 0
    if not 0 in index_of_sorted2: # <---- lol why were these two conditionals so hard to figure out
        min = 0                   # <-----also I know my sort is 2 methods technically but it made more
    else:                         #       sense to do it like this plz dont penalize
        min = 1                   #       Also this is way more efficient than the one described in class
    for i in range(len(not_sorted2)):
        if not_sorted2[i] < not_sorted2[min] and not i in index_of_sorted2:
            min = i
        # else:
        #     min = 1
            
    # is_sorted += [not_sorted[min]]
    # print(is_sorted)
    to_return = [min, not_sorted2[min]] 
    # print(to_return)
    return to_return

parser = argparse.ArgumentParser(description='This script sorts the list of docking energies file')

parser.add_argument("--f", required= True, type= str, help="name of file")
args = parser.parse_args()
file_name = args.f
file = open(file_name, "r")
#file = open("tom_k_doc_ene.txt", "r")
lines = file.readlines()
dictio = {}
names = []
energies = []
sorted_names = []
sorted_energies = []
for line in lines:
    s = line.split() #[0] = ligand name [1] = energy
    name = s[0]
    energy = s[1]
    names += [name]
    energies += [energy]
    dictio[name] = float(energy)
    # print(s)
output = custom_sort(energies, names)
output_names = output[1]
output_energies = output[0]
# for i in range(len(names)):
#     print(output_names[i] + "   "+ output_energies[i])
print(output_names)
print(len(output_names))
print(output_energies)
print(len(output_energies))
# print(dictio)

quit()