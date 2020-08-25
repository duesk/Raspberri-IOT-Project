import os
import glob
from pathlib import Path


def check_usb_files(): 
    home = str(Path.home())
    print("ruta de home")
    print(home)
    gcodes = [] 
    file_list = os.listdir(home+"/usb")
    for file in file_list:
        if file.endswith(".gcode"):
            gcodes.append(file)
        print(file)
    return gcodes

def check_sd_files():
    home = str(Path.home())
    print("ruta de home")
    print(home)
    gcodes = [] 
    file_list = os.listdir(home+"/gcodes")
    for file in file_list:
        if file.endswith(".gcode"):
            gcodes.append(file)
        print(file)
    return gcodes



#os.system("mount /dev/sda1 /UBS")