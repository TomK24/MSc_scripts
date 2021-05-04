#!/usr/bin/python

#########################################################
# Created by Thomas Kenyon, 2020

#This script generates the undordered csv file with my docking h bond occupancy data.
#In hindsight, there was no reason I had to write the code to make a csv file like this from scratch
#########################################################

import os
import sys


res_wt = ["VAL7", "ASP8", "PHE13", "LEU19", "ASP49", "HIS57", "TRP68", "HIS71", "LYS96", "ALA102", "ILE133", "ALA134", "ARG137", "CYS138", "VAL139"] 
file = open("report.txt", "r")
filel = file.readlines()
file.close()
info = {}
ligands = []

file2 = open("ligs.txt", "r")
passed1 = file2.readlines()
file2.close()
passed = []
for line in passed1:
    new = line.strip()
    new2 = new[:-4]
    passed += [new2]
for line in filel:
    if not line.startswith("SANC") and not line.startswith("PZA"):
        continue
    items = line.split()
    name1 = items[0][:-6]
    if not name1 in passed:
        continue
    energy = items[3]
    hbonds = []
    if len(items) == 7: #hbonds present
        hbonds1 = items[6]
        hbonds2 = hbonds1.strip()
        hbonds3 = hbonds2.split(",")
    name = ""
    if name1.endswith("le"):
        name += name1[:-6] + "_le"
    elif name1.endswith("lc"):
        name += name1[:-6] + "_lc"
    else:
        name += name1[:-3]
    # Got all data now.
    info[name] = [energy, hbonds3]
    ligands += [name]
ordered = []
numbers = []
for i in ligands:
    if "PZA" in i:
        continue
    number = i[6] + i[7] + i[8]
    numbers += [int(number)]
numbers.sort()
ordered += []
# last = 0
# for i in numbers()
#     current = i
#     if not last = 0:
#         last = current
#     if current == last:
duplicates = []
last = 0
for i in numbers:
    current = i
    if last == 0:
        last = current
        continue
    else:
        if current == last:
            duplicates += [current]
    last = current
prev = 0
for i in numbers:
    if i == prev:
        continue
    if i in duplicates:
        new_le = "SANC00" + str(i) + "_le"
        new_lc = "SANC00" + str(i) + "_lc"
        ordered += [new_le]
        ordered += [new_lc]
    else:
        # new = "SANC00" + str(i)
        # ordered += [new]
        for x in passed:
            num = str(i)
            if num in x:
                name = ""
                if x.endswith("le"):
                    name += "SANC00" + str(i) + "_le"
                    ordered += [name]
                elif x.endswith("lc"):
                    name += "SANC00" + str(i) + "_lc"
                    ordered += [name]
                else:
                    name += "SANC00" + str(i)
                    ordered += [name]
    prev = i

header1 = ","
for i in res_wt:
    header1 += i + ","
header = header1[:-1] + "\n"
output = [header]
for i in ordered: # FOR EACH ligand
    new_line = i + ","
    hbonds4 = info[i][1]
    for i in res_wt:
        if i in hbonds4:
            new_line += "1.0,"
        else:
            new_line += "0.0,"
    new_line1 = new_line[:-1]
    output += [new_line1 + "\n"]

csv = open("hbond.csv", "w")
csv.writelines(output)
csv.close()


        







            

# systems = []
# sys_file = open("systems.txt", "r")
# systems2 = sys_file.readlines()
# for line in systems2:
#     systems += [line.strip()]


# files = os.listdir("./")
# os.system("mkdir sorted_cpptraj")
# ligands_file = open("ligands.txt", "r")
# ligands2 = ligands_file.readlines()
# ligands = []
# for ligand in ligands2:
#     if not ligand == "" and not ligand == "\n": 
#         ligands += [ligand.strip()]
# ligands_file.close()
# for ligand in ligands:
#     os.system("mkdir ./sorted_cpptraj/{ligand}".format(**locals()))
#     for folder in files:
#         if os.path.isdir("./" + folder) and not folder.startswith("sorted"):
#             os.chdir("./{folder}".format(**locals()))
#             files2 = os.listdir("./")
#             for file in files2:
#                 if ligand in file:
#                     os.system("cp {file} ../sorted_cpptraj/{ligand}".format(**locals()))
#                     os.system("mv ../sorted_cpptraj/{ligand}/{file} ../sorted_cpptraj/{ligand}/{folder}.dat".format(**locals()))
#             os.chdir("../".format(**locals()))
# os.chdir("./sorted_cpptraj")
# files3 = os.listdir("./")
# for folder in files3:
#     if os.path.isdir("./" + folder):
#         os.chdir("./{folder}".format(**locals()))
#         files4 = os.listdir("./")
#         for dat in files4:
#             datl = dat[:-4]
#             #print(os.getcwd())
#             os.system('''grep "UNK" {dat} > {datl}.txt'''.format(**locals()))
#             os.system("rm {dat}".format(**locals()))
#             file1 = open(datl +".txt", "r")
#             file2 = file1.readlines()
#             file1.close()
#             edited = edit(file2)
#             file3 = open(datl + ".txt", "w")
#             file3.writelines(edited)
#             file3.close()
#             # new_csv = make_csv()
#             # csv_file = open("output.csv", "w")
#             # csv_file.writelines(new_csv)
#             # csv_file.close()
#         os.chdir("../")
        
# for folder in files3:
#     if os.path.isdir("./" + folder):
#         print(folder)
#         os.chdir("./{folder}".format(**locals()))
#         new_csv = make_csv()
#         csv_file = open("output.csv", "w")
#         csv_file.writelines(new_csv)
#         csv_file.close()
#     os.chdir("../")


            



print("All done!!")



        
