#!/usr/bin/python3

import argparse
import os
import re

parser = argparse.ArgumentParser(description="This script runs process_VSResults.py on all the .dlg files in a given directory. Because the .py script crashes as soon as there's more than 1 .dlg file in a directory because whoever wrote it did a half-assed job. So it needs this script to babysit it by basically choosing a .dlg file in a given directory and then puting it in its own directory alone and feeding that to this script. Then it moves the output .pdbqt files into the output folder and deletes the temp folder. for every .dlg file. Yay.")

parser.add_argument("--d", required= True, type= str, help="Name of directory with all.dlg files")
parser.add_argument("--r", required= True, type= str, help="This is the full name of the receptor in pdbqt format")
# parser.add_argument("--g", required= False, default='100', type= str, help="This is the number of GA runs. If left blank it defaults to 100")
# parser.add_argument("--z", required= True, default='100', type= str, help="filename of the original pdb file, need this to extract active site coords")
args = parser.parse_args()
folder_name = args.d
receptor_name = args.r
os.system("mkdir output")
files = os.listdir("./{folder_name}".format(**locals()))
for filename in files: #Loop through all .dlg files. For each one copy into temp folder and receptor pdbqt, Run script passing temp folder to it
    if filename.endswith(".dlg"): #Then copy output pdbqts to output folder. delete temp folder. What a dumb workaround
        # print(file)
    #*************************************LOGIC*******************************************
    # Directory structure: script folder (DLG folder | temp folder | output folder)
        os.system("mkdir temp")
        os.chdir("./{folder_name}".format(**locals()))
        os.system("cp {filename} -t ../temp".format(**locals()))
        os.system("cp {receptor_name} -t ../temp".format(**locals()))
        os.chdir("../")
        os.system("process_VSResults.py -d temp -r {receptor_filename} -t 2.0 -x -1 -D -p".format(**locals()))
        os.chdir("./output")
        os.system("cp ../temp/*lc.pdbqt .")
        os.system("cp ../temp/*le.pdbqt .")
        os.chdir("../")
        print("{filename}".format(**locals()))

        os.system("rm -r temp")
    #*************************************************************************************
print("done!")
quit()