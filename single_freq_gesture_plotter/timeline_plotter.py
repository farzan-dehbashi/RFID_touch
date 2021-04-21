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

def plot(times,RSSIs, out_dir, name):
    # axes = plt.gca()
    # axes.set_ylim([-65,-45])
    #
    plt.xlabel("Time")
    plt.ylabel("RSSI")
    #
    plt.grid()
    #
    # rc('font',**{'family':'serif','serif':['Times']})
    # rc('text', usetex=True)

    plt.plot(times,RSSIs, color="red", linestyle='--', marker='o')
    plt.savefig(str(out_dir)+ '/' + str(name) + ".png", dpi=500)

    plt.clf()



parser = argparse.ArgumentParser(description= 'This code reads from a reading directory (in) and plots each of gestures included in that directory in an html file. The style of this plot is a timeline for each tag which is hardcoded in the program.')
parser.add_argument('-i', '--inputdirectory', type= str, metavar='', required= False, help='input directory')
parser.add_argument( '-m', '--html', action='store_true', required= False, help='if active, makes an html file')
args = parser.parse_args()



############## initiating the vars
in_dir = 'in'
out_dir = 'out'
tags = ['0x00e200600322e139f7000000','0x00e200600322e19c64000000']
#'0x2d0500600322e19266000000','0x00e200600322e08d91000000'
############## changing the command line vars
if args.inputdirectory:
    in_dir = args.inputdirectory

############## find all csv files in the input directory
gestures = [file
    for path, subdir, files in os.walk(in_dir)
    for file in glob(os.path.join(path, '*.csv'))]

for gesture in gestures: #iterating over the all files in the input directory
    df = pd.read_csv(gesture, names=["EPCValue", "TimeStamp", "RunNum", "RSSI", "Reader", "Frequency", "Power", "Antenna"])
    df = df.iloc[5:] #cleaning the first lines

    for tag in tags:
        filt = (df['EPCValue'] == str(tag))
        filtered_df = df.loc[filt]

        times = filtered_df['TimeStamp'].tolist()
        RSSIs = filtered_df['RSSI'].tolist()

        time_stamp = []
        start_time = datetime.fromtimestamp(float(times[0]))
        for i in range(0, len(times)):  # converts lists of time stamps and rssis to int and float
            times[i] = float(times[i])
            time_stamp = datetime.fromtimestamp(times[i])
            times[i] = time_stamp - start_time  # indicates each sample time to be sample timestamp - start time
            times[i] = float(times[i].total_seconds())  # convert the result to seconds
            RSSIs[i] = float(RSSIs[i])

        plot(times,RSSIs, out_dir, tag)

############## html maker
if args.html:
    doc = dominate.document(title='')

    with doc.head:
        link(rel='stylesheet', href='style.css')
        script(type='text/javascript', src='script.js')

    with doc:
        with div(id='header').add(ol()):
            for i in ['home', 'about', 'contact']:
                li(a(i.title(), href='/%s.html' % i))

        with div():
            attr(cls='body')
            p('Lorem ipsum..')

    print(doc)


