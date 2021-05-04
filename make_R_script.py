#!/usr/bin/python3

#########################################################
# Created by Thomas Kenyon, 2020

#This is a messy script, I need to clean it up by seperating redundant loginc into functions.
#########################################################

import os
import re
wd = os.getcwd()
# insert = full name
# replace = short name (just number)
field_1 = '''  Lreplace = read.table('replace.csv',sep=' ', header = FALSE, quote="'", stringsAsFactors=FALSE, fill=TRUE)\n'''
field_2_1st = '''  rmsd_frame = list(Lreplace = Lreplace$V1,\n'''
field_2_middle = '''                    Lreplace = Lreplace$V1,\n'''
field_2_end = '''                    Lreplace = Lreplace$V1)\n'''
field_3 = '''  rmsd_Lreplace <- rep("insert",length(Lreplace$V1))\n'''
field_4 = '''  Breplace = cbind(RMSD = rmsd_frame$Lreplace,rmsd_Lreplace)\n'''
long_field_1 = "  rmsd_data_1 = rbind("
files = os.listdir("./")
template_file = open("template.R", "r")
template = template_file.readlines()
new_R = []
control = "PZA"
#MAKE list of ligands/MD systems
csv_files_1 = []
csv_names_1 = []
for file in files:
    if file.endswith(".csv") and not "lig_rmsd_all" in file and not control in file:
        csv_files_1 += [file]
        csv_names_1 += [file[:-4]]
csv_numbers_1 = []
for i in csv_names_1:
    if i.endswith("le") or i.endswith("lc"):
        number_1 = int(i[6:-3])
        csv_numbers_1 += [number_1]
    else:
        number_1 = int(i[6:])
        csv_numbers_1 += [number_1]

csv_numbers_1.sort()
csv_numbers = [str(i) for i in csv_numbers_1]
duplicates = []
counted = []
any_duplicates = False
for i in csv_numbers:
    if i in counted:
        duplicates += [i]
        any_duplicates = True
    counted += [i]
duplicates_full = []
for i in duplicates:
    duplicates_full += ["SANC00{i}_le".format(**locals())]
    duplicates_full += ["SANC00{i}_lc".format(**locals())]
suffixes = [] # must be sorted.
second_duplicate = False
for i in csv_numbers:
    suffix = None
    if i in duplicates and second_duplicate == False:
        suffix = "_le"
        second_duplicate = True
    elif second_duplicate == True:
        suffix = "_lc"
        second_duplicate = False
    else:
        for name in csv_names_1:
            if i in name:
                if "_le" in name:
                    suffix = "_le"
                    break
                elif "_lc" in name:
                    suffix = "_lc"
                    break
                else:
                    suffix = ""
                    break
    suffixes += [suffix]
csv_numbers.insert(0, control)
suffixes.insert(0, "")
csv_files = []
csv_names = []
jup_list = []
for i in range(len(csv_numbers)):
    if "PZA" in csv_numbers[i]:
        csv_files += [csv_numbers[i] + suffixes[i] + ".csv"]
        csv_names += [csv_numbers[i]]
        jup_list += [csv_numbers[i]]
    else:
        csv_files += ["SANC00" + csv_numbers[i] + suffixes[i] + ".csv"]
        csv_names += ["SANC00" + csv_numbers[i] + suffixes[i]]
        if any_duplicates == False:
            jup_list += ["SANC00" + csv_numbers[i]]
        else:
            jup_list += ["SANC00" + csv_numbers[i] + suffixes[i]]
list1 = []
for l in jup_list:
    entry2 = l
    if entry2 in duplicates_full:
        entry = entry2
        list1 += '''"{entry}": "y", '''.format(**locals())
    elif entry2.endswith("_le") or entry2.endswith("_lc") :
        entry = entry2[:-3]
        list1 += '''"{entry}": "y", '''.format(**locals())
    else:
        entry = entry2
        list1 += '''"{entry}": "y", '''.format(**locals())
            
list_file = open("list2.txt", "w")
list_file.writelines(list1)
list_file.close()
# START generating new file:
for idx in range(len(template)):
    line = template[idx]
    in_field_1 = False
    done_field_1 = False

    in_field_2 = False
    done_field_2 = False

    in_field_3 = False
    done_field_3 = False

    in_field_4 = False
    done_field_4 = False

    if line.startswith("  setwd('"):
        new_R += ["  setwd('{wd}')\n".format(**locals())]
    elif "#START_FIELD_1" in line:
        new_R += [line]
        for system in csv_names:
            new_line = field_1.replace("replace", system)
            new_R += [new_line]
    # elif "#END_FIELD_1" in line:
    #     new_R += [line]
    elif "#START_FIELD_2" in line:
        new_R += [line]
        for i in range(len(csv_names)):
            name = csv_names[i]
            if i == 0:
                new_line = field_2_1st.replace("replace", name)
                new_R += [new_line]
            elif i == len(csv_names)-1:
                new_line = field_2_end.replace("replace", name)
                new_R += [new_line]
            else:
                new_line = field_2_middle.replace("replace", name)
                new_R += [new_line]
    # elif "#END_FIELD_2" in line:
    #     new_R += [line]
    elif "#START_FIELD_3" in line:
        new_R += [line]
        if any_duplicates == False or any_duplicates == True:
            for system in csv_names:
                if system in duplicates_full:
                #if system.endswith("_le") or system.endswith("_lc"):
                    new_line = field_3.replace("replace", system).replace("insert", system)
                    new_R += [new_line]
                elif system.endswith("_le") or system.endswith("_lc"):
                    new_line = field_3.replace("replace", system).replace("insert", system[:-3])
                    new_R += [new_line]
                else:
                    new_line = field_3.replace("replace", system).replace("insert", system)
                    new_R += [new_line]
        else:
            for system in csv_names:
                new_line = field_3.replace("replace", system).replace("insert", system)
                new_R += [new_line]
    # elif "#END_FIELD_1" in line:
    #     new_R += [line]
    elif "#START_FIELD_4" in line:
        new_R += [line]
        for system in csv_names:
            new_line = field_4.replace("replace", system)
            new_R += [new_line]
    # elif "#END_FIELD_4" in line:
    #     new_R += [line]
    elif "  #START_LONG_FIELD" in line:
        for system in csv_names:
            new_entry = "B{system}, ".format(**locals())
            long_field_1 += new_entry
        long_field = long_field_1[:-2] + ")\n"
        new_R += [long_field]
    else:
        new_R += [line]
for system in csv_names:
    new_entry = "B{system}, ".format(**locals())
    long_field_1 += new_entry
long_field = long_field_1[:-2] + ")\n"
new_file = open("test_R.R", "w")
new_file.writelines(new_R)
new_file.close()
print("done!")
quit()
