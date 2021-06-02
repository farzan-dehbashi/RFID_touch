#!/usr/bin/env
# Author: Farzan Dehbashi
# Date: 05/02/2021
# Description: This script will acquire the log files from an RFID reader as some routines based on instructions that user implies in tasks.csv file
# Date Modified: 05/02/2021

######################## imports begin
import matplotlib
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import dominate
from dominate.tags import *
import sys
import os
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.font_manager import FontProperties
import cv2
import time
import subprocess
########################imports ends

def read_instructions(instruction_file):
    column_names = [ "TYPE", "FIXED_LENGTH", "LENGTH", "START_TIME", "END_TIME", "RESULTS_PATH", "DESCRIPTIONS"]  # sets the names of columns
    instructions_sheet = pd.read_csv(instruction_file, names=column_names, delimiter="\t")
    instructions_sheet = instructions_sheet.iloc[1:]
    return instructions_sheet
########################read_instructions ends

def run(instructions_sheet, out_dir, ip):
    for i, instruction in instructions_sheet.iterrows():
        if instruction['FIXED_LENGTH'] == "T":
            if instruction['TYPE'] == "S": # type is sleep and specific length
                instruction['START_TIME'] = str(datetime.now())
                time.sleep(float(instruction['LENGTH']))
                instruction['END_TIME'] = str(datetime.now())

            elif instruction['TYPE'] == "R": # type is run and specific length
                path = str(out_dir)+"/"+str(instruction['RESULTS_PATH'])
                instruction['START_TIME'] = datetime.now()
                #runs the bash script which runs the
                os.system("./script.bash "+str(path)+" "+str(ip)+" &")
                time.sleep(float(instruction['LENGTH']))
                os.system("ps -ef | grep script.bash | grep -v grep | awk '{print $2}' | xargs kill -9") #ends the process in the bash script
                instruction['END_TIME'] = datetime.now()
            else:
                print("instruction "+str(instruction)+"\n Type is not recognized")
        elif instruction['FIXED_LENGTH'] == "F":
            instruction['START_TIME'] = datetime.now()
            os.system("./script.bash &")
            input("press any key to finish this trial")
            os.system("ps -ef | grep script.bash | grep -v grep | awk '{print $2}' | xargs kill -9")
            instruction['END_TIME'] = datetime.now()
        else:
            print("instruction "+str(instruction)+"\n FIXED_LENGTH is not recognized")

    #update csv file
    instructions_sheet.to_csv("instructions_log.csv")

######################## run ends


######################## main begin
if __name__ == "__main__":
     instructions_sheet = read_instructions(sys.argv[1]) # returns a pandas data frame which contains a sheet of all instructions
     run(instructions_sheet, sys.argv[2], sys.argv[3])
     print(instructions_sheet.head())

######################## main ends