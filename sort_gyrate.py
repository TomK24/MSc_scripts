#!/usr/bin/python3


import os
import sys
import re
def edit(file):
    new_file = []
    for line in file:
        line2 = line.split()
        frac = line2[4]
        frac = float(frac)
        if frac > 0.01:
            new_file += line
    return new_file

def make_csv():
    #res_wt = ["VAL_7", "ASP_8", "GLY_8", "PHE_13", "LEU_19", "ASP_49", "ALA_49", "GLY_49", "HIS_57", "PRO_57", "TRP_68", "HIS_71", "LYS_96", "ALA_102", "ILE_133", "ALA_134", "VAL_134", "ARG_137", "HIS_137", "CYS_138", "VAL_139", "MET_139"]
    res_wt = ["VAL7", "ASP8", "GLY8", "PHE13", "LEU19", "ASP49", "ALA49", "GLY49", "HIS57", "PRO57", "TRP68", "HIS71", "LYS96", "ALA102", "ILE133", "ALA134", "VAL134", "ARG137", "HIS137", "CYS138", "VAL139", "MET139"]
    res_mut = ["GLY_8", "ALA_49", "GLY_49", "PRO_57", "VAL_134", "ARG_137", "MET_139"]
    files = os.listdir("./")
    csv_dict = {}
    
    for file in files:
        if file.endswith(".txt"):
            res_dict = {}
            txt_file = open(file, "r")
            txt = txt_file.readlines()
            txt_file.close()
            res_txt = []
            count = 0
            for line2 in txt:
                line = line2.replace("_", "")
                for res in res_wt:
                    if res in line:
                        res_txt += [line]
                        if count == 0:
                            res_dict[file[:-4]] = [res]
                        else:
                            res_dict[file[:-4]] += [res]
            res_frac = {}
            for line in res_txt:
                line2 = line.split()
                zero = line2[0]
                one = line2[1]
                res = ""
                if not "UNK" in zero:
                    res3 = zero
                    res2 = res3.split("@")
                    res += res2[0].replace("_", "")
                else:
                    res3 = one
                    res2 = res3.split("@")
                    res += res2[0].replace("_", "")
                frac = line2[4]
                #frac = float(frac)
                res_frac[res] = frac
        name = file[:-4]
        csv_dict[name] = res_frac
    
    csvl = []
    header = ","
    for res in res_wt:
        header += "{res},".format(**locals())
    csvl += [header[:-1] + "\n"]
    for system in systems:
        new_line = "{system},".format(**locals())
        #new_line = ""
        temp_dict = csv_dict[system]
        keys = temp_dict.keys()
        for res in res_wt:
            if res in keys:
                frac2 = float(temp_dict[res]) * 100
                frac = frac2 # why does Seaborn/Pandas crash and burn if I convert this to a int here????
                new_line += "{frac},".format(**locals())
            else:
                new_line += "0,"
        csvl += [new_line[:-1] + "\n"]
    return csvl

                
            

systems = []
sys_file = open("systems.txt", "r")
systems2 = sys_file.readlines()
for line in systems2:
    systems += [line.strip()]


files = os.listdir("./")
os.system("mkdir sorted")
ligands_file = open("ligands.txt", "r")
ligands2 = ligands_file.readlines()
ligands = []
for ligand in ligands2:
    if not ligand == "" and not ligand == "\n": 
        ligands += [ligand.strip()]
ligands_file.close()
for ligand in ligands:
    os.system("mkdir ./sorted/{ligand}".format(**locals()))
    for folder in files:
        if os.path.isdir("./" + folder) and not folder.startswith("sorted"):
            os.chdir("./{folder}".format(**locals()))
            files2 = os.listdir("./")
            for file in files2:
                if ligand in file:
                    os.system("cp {file} ../sorted/{ligand}".format(**locals()))
                    os.system("mv ../sorted/{ligand}/{file} ../sorted/{ligand}/{folder}.xvg".format(**locals()))
            os.chdir("../".format(**locals()))
os.chdir("./sorted")
files3 = os.listdir("./")
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
        
for folder in files3:
    if os.path.isdir("./" + folder):
        # print(folder)
        os.chdir("./{folder}".format(**locals()))
        # new_csv = make_csv()
        # csv_file = open("output.csv", "w")
        # csv_file.writelines(new_csv)
        # csv_file.close()
        xvg=os.listdir('./')
        for i in xvg:
            if ".xvg" in i:
                xvg_name=i[:-4]
                os.system("cat "+i+" | tail -n+19 | awk '{print $2}' > "+xvg_name+".csv")
            else:
                pass
        os.system("rm *.xvg")
        csvv=os.listdir('./')
        for i in csvv:
            name = i
            file = open(name, "r")
            csv = file.readlines()
            file.close()
            x = csv[0].strip()
            new_csv = []
            for i in range(len(csv)):
                x = csv[i].strip()
                if x.isdigit() == True or "." in x:
                    new_csv += [x + "\n"]
            new_file = open(name, "w")
            new_file.writelines(new_csv)
            new_file.close()
    os.chdir("../")


            



print("All done!!")



        
