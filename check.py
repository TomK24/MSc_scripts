#!/usr/bin/python
import re
import sys
import os
import glob
import subprocess
from os import listdir
from itertools import islice
# from subprocess import Popen, PIPE
# sys.stdout = open("test_stdout.txt", "w")
def get_files():
    os.chdir("./VMD")
    files = os.listdir("./")
    pdb_list = []
    xtc_list = []
    pdbxtc = {}
    for file in files:
        if file.endswith(".pdb"):
            pdb_list += [file]
        elif file.endswith(".xtc"):
            xtc_list += [file]
    for pdb in pdb_list:
        ligand = pdb[4:-4]
        for xtc in xtc_list:
            if ligand in xtc:
                pdbxtc[pdb] = xtc
    os.chdir("../")
    return pdbxtc
def edit_PBS(pdbxtc):
    os.chdir("./VMD")
    old_pbs = []
    old_pbs += pbs
    replace = "replace"
    pdbs = []
    for key in pdbxtc:
        pdbs += [key]
    wd = os.getcwd()
    wd1 = wd.split("/")
    wd2 = wd1[len(wd1)-3]
    old_pbs[1] = old_pbs[1].replace(replace, wd2)
    old_pbs[7] = old_pbs[7].replace(replace, wd)
    old_pbs[8] = old_pbs[8].replace(replace, wd)
    old_pbs[20] = old_pbs[20].replace(replace, wd)

    for pdb in pdbs:
        new = string
        new_line = new.replace("rep1", pdb).replace("rep2", pdbxtc[pdb]).replace("rep3", pdb[4:-4]).replace("rep4", pdb[4:-4]) + "\n"
        old_pbs += [new_line]
    new_pbs = open("cpptraj.pbs", "w")
    new_pbs.writelines(old_pbs)
    new_pbs.close()
    os.system("qsub cpptraj.pbs")
    os.system("Job submitted!")
    os.chdir("../")

def move_files():
    os.chdir("./VMD")
    files = os.listdir("./")
    count = 0
    wd2 = wd
    spec_path2 = os.getcwd()
    spec_path = spec_path2.split("/")
    spec = spec_path[len(spec_path)-3]
    os.system("mkdir {wd2}/cpptraj/{spec}".format(**locals()))
    for file in files:
        if "average" in file and file.endswith(".dat"):
            os.system("cp {file} {wd2}/cpptraj/{spec}".format(**locals()))
            count += 1
    os.chdir("../")
    return count



#     #old_pbs[30] = old_pbs[30].replace(replace, cleaned_name)

#string = "echo $'parm rep1\ntrajin rep2\nhbond :1-187 out hbond_rep3.dat avgout hbond_average_rep4.dat image\nrun\nquit\n' | cpptraj"

# wd = os.getcwd() #working dir where script is run from
# working_folder1 = wd.split("/")
# working_folder = working_folder1[len(working_folder1)-1] #folder 
# replace = "replace"
#rmsd_replace = 
# if not os.path.isdir("cpptraj"):
#     os.system("mkdir cpptraj")
files = os.listdir("./")
# Open every folder in working dir. Then open any subfolder that starts with "sub". In there, check if there is a MD_0_1.log file. If not, report it. If there is, open it and check if last line starts with "Finished mdrun " and its size is 9.1mb or greater. If it isnt, report it.

#perhaps also check for corresponding analysis files hm. Perhaps check log files and store info. then for log files that are complete. check that all analysis files in ../analysis/[GYRATE/VMD,RMSD etc etc] are there. If not, report that.
# pbs_file = open("cpptraj.pbs", "r")
# pbs = pbs_file.readlines()
# pbs_file.close()
complete_logs = {}
incomplete_logs = {}
no_logs = {}
for folder in files:
    if os.path.isdir("./" + folder):
        os.chdir("./{folder}".format(**locals()))
        files2 = os.listdir("./")
        complete_log_count = 0
        incomplete_log_count = 0
        no_log_count = 0
        for folder2 in files2:
            if os.path.isdir("./" + folder2) and folder2.startswith("sub"):
                os.chdir("./{folder2}".format(**locals())) #into folder
                sub_files = os.listdir("./")
                found_log = False
                wd = os.getcwd()
                wd_split = wd.split("/")
                ligand = wd_split[len(wd_split)-1][4:]
                system = wd_split[len(wd_split)-2]
                for file in sub_files:
                    if file == "md_0_1.log":
                        found_log = True
                        log_file = open("md_0_1.log", "r")
                        log = log_file.readlines()
                        log_file.close()
                        size = os.path.getsize("./md_0_1.log")
                        last_line = log[len(log)-1]
                        if last_line.startswith("Finished mdrun"): #IF log file is present AND complete
                            if complete_log_count == 0:
                                complete_logs[system] = [ligand]
                                complete_log_count += 1
                            else:
                                complete_logs[system] += [ligand]
                                complete_log_count += 1
                        else:#                                         IF log file is present BUT incomplete 
                            if incomplete_log_count == 0:
                                incomplete_logs[system] = [ligand]
                                incomplete_log_count += 1
                            else:
                                incomplete_logs[system] += [ligand]
                                incomplete_log_count += 1
                if not found_log:#                                      If log file is ABSENT
                    if no_log_count == 0:
                        no_logs[system] = [ligand]
                        no_log_count += 1
                    else:
                        no_logs[system] += [ligand]
                        no_log_count += 1
                os.chdir("../")
        os.chdir("../")

print("                               Completed logs:")
for key in complete_logs:
    print("System: {key}".format(**locals()))
    lst = complete_logs[key]
    for i in lst:
        print("  -" + i)

print("\n\n                              Incomplete logs:")
for key in incomplete_logs:
    print("System: {key}".format(**locals()))
    lst = incomplete_logs[key]
    for i in lst:
        print("  -" + i)

print("\n\n                                Missing logs:")
for key in no_logs:
    print("System: {key}".format(**locals()))
    lst = no_logs[key]
    for i in lst:
        print("  -" + i)

        # if found_VMD == False:
        #     print("Did not find a VMD folder in this analysis folder:\n{wd}/{file}".format(**locals()))
        #     os.chdir("../")                #out of folder (only if no VMD folder found)

    # elif os.path.isdir(wd + "/" +file) and not file == "cpptraj":# If folder, go into it and check for an analysis folder
    #     wd2 = os.getcwd()
    #     os.chdir("{file}".format(**locals())) #into folder
    #     files2 = os.listdir("./")
    #     if len(files2) == 0:
    #         os.chdir("../")
    #     found_analysis = False
    #     for file2 in files2:
    #         if file2 == "analysis": #Check for analysis folder
    #             found_VMD = False
    #             found_analysis = True
    #             os.chdir("./{file2}".format(**locals())) #into folder
    #             files3 = os.listdir("./")
    #             for file3 in files3:
    #                 if file3 == "VMD": #Check for VMD folder
    #                     found_VMD = True
    #                     #print("Found a VMD folder here:\n{wd}/{file}/{file2}/{file3}".format(**locals()))
    #                     #test = get_files()
    #                     #print(test)
    #                     #edit_PBS(test)
    #                     count = move_files()
    #                     print("found {count} files in:\n{wd}/{file}/{file2}/{file3}. Copying them".format(**locals()))
    #                     os.chdir("../")                #out of folder
    #                     os.chdir("../")                #out of folder
    #                     break
    #             if found_VMD == False:
    #                 print("Did not find a VMD folder here:\n{wd}/{file}/{file2}".format(**locals()))
    #                 os.chdir("../")                #out of folder
    #                 os.chdir("../")                #out of folder
    #     if not found_analysis:
    #         print("Did not find a analysis folder here:\n{wd}/{file}".format(**locals()))
    #         os.chdir("../")
        
    #print(file)
    # os.chdir("./sub_files")
        #os.system("cp md_extend.pbs  ./{file}".format(**locals()))
        #os.chdir("../")
#print("Done moving...\nStarting .pbs editing...")
# for folder in files:
#     if not folder.startswith("sub_"):
#         continue
#     cleaned_name = folder[4:]
#     number = folder[10] + folder[11] + folder[12]
#     if "PZA" in folder:
#         number = "PZA"
#     # print(cleaned_name)
#     working_dir = working_dir_pre + "/" + folder
#     os.chdir("./{folder}".format(**locals()))
#     pbs_file = open("md_extend.pbs", "r")
#     old_pbs = pbs_file.readlines()
#     pbs_file.close()
#     # print("opened pbs!")
#     old_pbs[1] = old_pbs[1].replace(replace, number)
#     old_pbs[7] = old_pbs[7].replace(replace, working_dir)
#     old_pbs[8] = old_pbs[8].replace(replace, working_dir)
#     old_pbs[20] = old_pbs[20].replace(replace, working_dir)

#     #old_pbs[30] = old_pbs[30].replace(replace, cleaned_name)
#     old_pbs[57] = old_pbs[57].replace(replace, cleaned_name)
#     old_pbs[58] = old_pbs[58].replace(replace, cleaned_name)
#     old_pbs[59] = old_pbs[59].replace(replace, cleaned_name)
#     old_pbs[60] = old_pbs[60].replace(replace, cleaned_name)
#     # old_pbs[58] = old_pbs[58].replace(replace, cleaned_name)
#     old_pbs[67] = old_pbs[67].replace(replace, cleaned_name)
#     old_pbs[68] = old_pbs[68].replace(replace, cleaned_name)
#     old_pbs[74] = old_pbs[74].replace(replace, cleaned_name)
#     pbs_file = open("md_extend.pbs", "w")
#     pbs_file.writelines(old_pbs)
#     pbs_file.close()

    #*********************DO editing here*****************************

    #*****************************************************************
    # os.chdir("../")
    # os.chdir("../")
# os.chdir("./cpptraj")
# print("all files copied into cpptraj folder. One folder per system containing all .dat files for that system")
# print("shortening names...")
# files = os.listdir("./")
# for file in files:
#     if os.path.isdir("./" + file):
#         os.chdir("./" + file)
#         files2 = os.listdir("./")
#         for file2 in files2:
#             new = file2[14:]
#             os.system("mv {file2} {new}".format(**locals()))
#         os.chdir("../")


print("done!")
# sys.stdout.close()
