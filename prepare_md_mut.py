#!/usr/bin/python
import re
import sys
import os
import glob
import subprocess
from os import listdir
# from subprocess import Popen, PIPE
# sys.stdout = open("test_stdout.txt", "w")
wd = os.getcwd()
working_dir_pre = wd
working_folder1 = wd.split("/")
working_folder = working_folder1[len(working_folder1)-1] #folder 
replace = "replace"
#rmsd_replace = 
files = os.listdir("./")
for file in files:
    if file.startswith("sub_"):
    #print(file)
    # os.chdir("./sub_files")
        os.system("cp md.pbs  ./{file}".format(**locals()))
        os.system("cp md.mdp  ./{file}".format(**locals()))
        os.system("cp npt.mdp  ./{file}".format(**locals()))
        os.system("cp nvt.mdp  ./{file}".format(**locals()))
        #os.chdir("../")
print("Done moving...\nStarting .pbs editing...")
for folder in files:
    if not folder.startswith("sub_"):
        continue
    cleaned_name = folder[4:]
    number = ""
    if "PZA" in folder:
        number = "PZA"
    else:
        number = folder[10] + folder[11] +folder[12]# + folder[9] + folder[10]
    
    # print(cleaned_name)
    working_dir = working_dir_pre + "/" + folder
    os.chdir("./{folder}".format(**locals()))
    pbs_file = open("md.pbs", "r")
    old_pbs = pbs_file.readlines()
    pbs_file.close()
    # print("opened pbs!")
    old_pbs[1] = old_pbs[1].replace(replace, number)
    old_pbs[7] = old_pbs[7].replace(replace, working_dir)
    old_pbs[8] = old_pbs[8].replace(replace, working_dir)
    old_pbs[20] = old_pbs[20].replace(replace, working_dir)

    #old_pbs[30] = old_pbs[30].replace(replace, cleaned_name)

    old_pbs[53] = old_pbs[53].replace(replace, cleaned_name)
    old_pbs[54] = old_pbs[54].replace(replace, cleaned_name)
    old_pbs[55] = old_pbs[55].replace(replace, cleaned_name)
    old_pbs[56] = old_pbs[56].replace(replace, cleaned_name)
    #old_pbs[57] = old_pbs[57].replace(replace, cleaned_name)
    #old_pbs[58] = old_pbs[58].replace(replace, cleaned_name)
    #old_pbs[59] = old_pbs[59].replace(replace, cleaned_name)
    #old_pbs[60] = old_pbs[60].replace(replace, cleaned_name)
    old_pbs[63] = old_pbs[63].replace(replace, cleaned_name)
    old_pbs[64] = old_pbs[64].replace(replace, cleaned_name)
    
    old_pbs[67] = old_pbs[67].replace(replace, cleaned_name)
    old_pbs[68] = old_pbs[68].replace(replace, cleaned_name)
    old_pbs[70] = old_pbs[70].replace(replace, cleaned_name)
    old_pbs[73] = old_pbs[73].replace(replace, cleaned_name)
    pbs_file = open("md.pbs", "w")
    pbs_file.writelines(old_pbs)
    pbs_file.close()

    #*********************DO editing here*****************************

    #*****************************************************************
    os.chdir("../")
    # os.chdir("../")



print("done!")
# sys.stdout.close()
