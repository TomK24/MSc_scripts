#!/usr/bin/python3

import os
import re

files = os.listdir("./")
os.system("mkdir converted")
folder = "converted"
name_list = []
extract_name = re.compile(r"SANC[0-9]+")
for filename in files:
    isLong = False
    if filename.endswith(".pdbqt"):# and filename.startswith("SANC"):
        # name = (re.search(extract_name, filename)).group()
        name = filename[:-6]
        # print(name)
        print("babel -ipdbqt {filename} -opdb {name}.pdb -h".format(**locals()))
        os.system("babel -ipdbqt {filename} -opdb {name}.pdb -h".format(**locals()))
        new_name = "{name}.pdb".format(**locals())
        name_list += [new_name + "\n"]
        #***Need to fix ATOM lines*******
        file = open("{name}.pdb".format(**locals()), "r")
        lines = file.readlines()
        file.close()
        #os.system("rm {name}.pdb".format(**locals()))
        new_pdb = []
        for line in lines:
            if line.startswith("ATOM") or line.startswith("HETATM") or line.startswith("END"):
                if line.startswith("ATOM"):
                    # prefix = "HETATM"
                    # edited_line = line[-5:]
                    new_line = line.replace("ATOM  ", "HETATM")
                    new_new_line = new_line.replace("LIG", "UNK")
                    new_pdb += [new_new_line]
                else:

                    new_pdb += [line.replace("LIG", "UNK")]
        #Need to do atom numbers now.
        new_new_pdb = []
        atom_types = []
        atom_numbers = []
        atoms = {}
        extract_atom = re.compile(r"[A-Z]{1,2}   UNK")
        for line in new_pdb:
            #print("input: " + line)
            if line.startswith("END"):
                break
            # atom_full = re.search(extract_atom, line).group() #Trying with regex
            # atom_less = atom_full.split()
            # atom = atom_less[0]
            atom_rough = line[12] + line[13]                   #Trying normally better (to get atom code)
            atom = atom_rough.replace(" ", "")
            edited_line = ""
            if not atom in atoms: #If atom not listed already, add it to dict and set number to 0
                atoms[atom] = 1
                if len(atom) == 1: #If first atom and atom length is 1 (ie C or O or N)
                    for e in range(len(line)):
                        if e == 14:
                            edited_line += "1"
                        elif e == 15:
                            edited_line += " "
                        else:
                            edited_line += line[e]
                    #new_line = line
                    #new_line[14] = 1
                else:              #IF first atom and atom length is 2 (ie BR or CL etc) LOL okay this is the same thing actually
                    for e in range(len(line)):
                        if e == 14:
                            edited_line += "1"
                        elif e == 15:
                            edited_line += " "
                        else:
                            edited_line += line[e]
            else:                      # IF atom type is listed, +1 to relevant atom type
                # idx = atom_types.index(atom)
                # atom_numbers[idx] += 1
                atoms[atom] += 1
                if atoms[atom] < 10:     #If atom # less than 10 
                    for e in range(len(line)):
                        if e == 14:
                            edited_line += str(atoms[atom])
                        elif e == 15:
                            edited_line += " "
                        else:
                            edited_line += line[e]
                elif atoms[atom] < 100:                  #If atom # is 10 or more but less than 100
                    temp = str(atoms[atom])
                    for e in range(len(line)):
                        if e == 14:
                            edited_line += temp[0]
                        elif e == 15:
                            edited_line += temp[1]
                        elif e == 16:
                            edited_line += " "
                        # elif e == 16:
                        #     continue
                        else:
                            edited_line += line[e]
                else:                                  #If atom # is more than 100 or more
                    temp = str(atoms[atom])
                    for e in range(len(line)):
                        if e == 14:
                            edited_line += temp[0]
                        elif e == 15:
                            edited_line += temp[1]
                        elif e == 16:
                            edited_line += temp[2]
                        # elif e == 16:
                        #     continue
                        else:
                            edited_line += line[e]   
                    # new_line = line
                    # num = str(atoms[atom])
                    # new_line[14] = num[0]
                    # new_line[15] = num[1]
                #*****Checking if there are any atom types with more than 99 atoms (need to move the column the left) NOT IMPLEMENTED YET AS OUR LIGANDS ARE ALL SMALL(ISH)
                for x in atoms:
                    if atoms[x] > 99:
                        isLong = True
            #print("output:  " + edited_line)
            #*******Need to ensure whatever 3 letter code is changed to UNK. VERY NB if removing the connect data like we are!!!

            edited_edited_line = ""
            if not isLong:
                for i in range(len(edited_line)):
                    if i == 17:
                        edited_edited_line += "U"
                    elif i == 18:
                        edited_edited_line += "N"
                    elif i == 19:
                        edited_edited_line += "K"
                    elif i == 25:
                        edited_edited_line += "1"
                    else:
                        edited_edited_line += edited_line[i]
            #**************************
            else:
                for i in range(len(edited_line)):
                    if i == 12:
                        continue
                    elif i == 16:
                        edited_edited_line += edited_line[i] + " "
                    elif i == 17:
                        edited_edited_line += "U"
                    elif i == 18:
                        edited_edited_line += "N"
                    elif i == 19:
                        edited_edited_line += "K"
                    elif i == 25:
                        edited_edited_line += "1"
                    else:
                        edited_edited_line += edited_line[i]    
            new_new_pdb += [edited_edited_line]
        #new_new_pdb += ["END\n"]
        new_new_new_pdb =[]
        for line in new_new_pdb:
            final_line = ""
            split_line = line.split()
            atom = split_line[10]
            if len(atom) == 2:
                atom1 = atom[0].capitalize()
                atom2 = atom[1].capitalize()
                for i in range(len(line)):
                    if i == 76:
                        final_line += atom1
                    elif i == 77:
                        final_line += atom2
                    else:
                        final_line += line[i]
                new_new_new_pdb += [final_line]
            else:
                new_new_new_pdb += [line]
        new_new_new_pdb += ["END\n"]

        #*************write final file*******************************
        new_file = open("{name}.pdb".format(**locals()), "w")
        new_file.writelines(new_new_new_pdb)
        new_file.close()
        ####
        os.system("mv {name}.pdb {folder}".format(**locals()))
file = open("ligands.txt", "w")
file.writelines(name_list)
file.close()
print("done!")
quit()
