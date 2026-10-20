#!/usr/bin/python
import re
import sys
import os
import glob
import subprocess
from os import listdir
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
    old_pbs = pbs
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
    os.chdir("../")


#     #old_pbs[30] = old_pbs[30].replace(replace, cleaned_name)

string = "echo $'parm rep1\ntrajin rep2\nhbond :1-187 out hbond_rep3.dat avgout hbond_average_rep4.dat image\nrun\\nq\\n' | cpptraj"

wd = os.getcwd()
working_dir_pre = wd
working_folder1 = wd.split("/")
working_folder = working_folder1[len(working_folder1)-1] #folder 
replace = "replace"
#rmsd_replace = 
files = os.listdir("./")
# Plan is to make a method that actually does the pbs editing. since it will be called multiple times at different locations in the code below. Will need to pass it what? Perhaps read the template PBS file and then write it and edit wherever appropriate?
pbs_file = open("cpptraj.pbs", "r")
pbs = pbs_file.readlines()
pbs_file.close()
for file in files:
    if file == "analysis":
        pass #Do analysis for VMD folder in here
        os.chdir("./{file}".format(**locals())) #into folder
        analysis_files = os.listdir("./")
        found_VMD = False
        for file2 in analysis_files:
            if file2 == "VMD":
                print("Found a VMD folder here:\n{wd}/{file}/{file2}".format(**locals()))
                test = get_files()
                #print(test)
                edit_PBS(test)
                os.chdir("../")                #out of folder
                found_VMD = True
                break
        if found_VMD == False:
            print("Did not find a VMD folder in this analysis folder:\n{wd}/{file}".format(**locals()))
            os.chdir("../")                #out of folder (only if no VMD folder found)

    elif os.path.isdir(wd + "/" +file):# If folder, go into it and check for an analysis folder
        wd2 = os.getcwd()
        os.chdir("{file}".format(**locals())) #into folder
        files2 = os.listdir("./")
        if len(files2) == 0:
            os.chdir("../")
        found_analysis = False
        for file2 in files2:
            if file2 == "analysis": #Check for analysis folder
                found_VMD = False
                found_analysis = True
                os.chdir("./{file2}".format(**locals())) #into folder
                files3 = os.listdir("./")
                for file3 in files3:
                    if file3 == "VMD": #Check for VMD folder
                        found_VMD = True
                        print("Found a VMD folder here:\n{wd}/{file}/{file2}/{file3}".format(**locals()))
                        test = get_files()
                        #print(test)
                        edit_PBS(test)
                        os.chdir("../")                #out of folder
                        os.chdir("../")                #out of folder
                        break
                if found_VMD == False:
                    print("Did not find a VMD folder here:\n{wd}/{file}/{file2}".format(**locals()))
                    os.chdir("../")                #out of folder
                    os.chdir("../")                #out of folder
        if not found_analysis:
            print("Did not find a analysis folder here:\n{wd}/{file}".format(**locals()))
            os.chdir("../")
        
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



print("done!")
# sys.stdout.close()
