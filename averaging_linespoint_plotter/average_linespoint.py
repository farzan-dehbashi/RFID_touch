import argparse
import dominate
import pandas as pd
from dominate.tags import *
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import rc
from glob import glob
import numpy as np




def create_df(width):
    columns = []
    for x in range(0, width):
        columns.append(str(x))
    df = pd.DataFrame(columns=columns)
    return df




parser = argparse.ArgumentParser(description= 'This code reads from a reading directory (in) and plots each of gestures included in that directory in an html file. The style of this plot is a timeline for each tag which is hardcoded in the program.')
parser.add_argument('-w', '--width', type=int, metavar='', required=True, help='sets width of the pad in cm (if width is 3 cm, 0,1,2 will be shown)')
parser.add_argument('-H', '--height', type=int, metavar='', required=True, help='sets height of the pad in cm (if height is 3 cm, 0,1,2 will be shown)')

args = parser.parse_args()


############## initiating the vars
in_dir = 'in'
out_dir = 'out'
tags = ['0x00e200600322e139f7000000','0x00e200600322e19c64000000']
width = args.width
height = args.height



############## find all csv files in the input directory
gestures = [file
    for path, subdir, files in os.walk(in_dir)
    for file in glob(os.path.join(path, '*.csv'))]

############## Initiate the result df


############## main

mean_df = create_df(width)  # contains an initial instance of the specific tag array csv file to store averages of that tag on it
std_df = create_df(width)

for gesture in gestures: #iterating over the all files in the input directory
    df = pd.read_csv(gesture, names=["EPCValue", "TimeStamp", "RunNum", "RSSI", "Reader", "Frequency", "Power", "Antenna"])
    df = df.iloc[5:] #cleaning the first lines

    x = str(gesture).split('_')[0].split('/')[1]
    y = str(gesture).split('_')[1].split('.')[0]

    for tag in tags: #iterates over all tags of the touch pad

        filt = (df['EPCValue'] == str(tag))
        filtered_df = df.loc[filt]

        RSSIs = filtered_df['RSSI']
        RSSIs = pd.to_numeric(RSSIs)

        mean_df.at[y, str(x)] = RSSIs.describe().loc['mean'] #adds to the result df
        std_df.at[y, str(x)] = RSSIs.describe().loc['std']

################# sorts the order of the result tables based on index
mean_df.sort_index(ascending=True).to_csv('./out/mean.csv')
std_df.sort_index(ascending=True).to_csv('./out/std.csv')


print('done')