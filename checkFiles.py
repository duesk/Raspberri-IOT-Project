import os
import glob
from pathlib import Path


def checkUSBFiles(): 
    listUSB = os.listdir("/media/rafael")
    print(listUSB)
    listUSB = os.listdir("/media/rafael/"+listUSB[0])
    print(listUSB)

    gcodes = []
    for file in listUSB:
        if file.endswith(".gcode"):
            gcodes.append(file)
    print(gcodes)
    return gcodes

def checkSDFiles():
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