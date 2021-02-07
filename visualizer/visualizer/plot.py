import matplotlib
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import dominate
from dominate.tags import *
import sys
import os
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import cv2

import pathlib

class Tag: # contains color and other necesities of the tag to be plotted
    def __init__(self, color, epc):
        self.color = color
        self.epc = epc
    def get_color(self):
        return self.color
    def get_epc(self):
        return self.epc

def read_gestures(directory): # read all log files of the experiments
    gesture_sheets = []
    with os.scandir(str(directory)) as gesture_directories:
        for gesture_directory in gesture_directories:
            if os.path.isdir(gesture_directory):
                sheet_name = str(directory)+"/"+str(gesture_directory.name)+"/"+str(gesture_directory.name)+".csv"
                column_names = ["EPCValue", "TimeStamp", "RunNum", "RSSI", "Reader", "Frequency", "Power", "Antenna"] #sets the names of columns
                sheet = pd.read_csv(sheet_name, names = column_names)
                sheet.name = str(gesture_directory.name)
                gesture_sheets.append(sheet)
    return gesture_sheets



def read_tags(tags_file_name): #this method reads all tags in the instruction file and return a list of tags
    tags_instruction = pd.read_csv(str(tags_file_name)) #reads the instruction file
    tags = []
    for index, row in tags_instruction.iterrows(): #adds tags to the tag list
        tag = Tag(row['COLOR'], row['EPCValue'])
        tags.append(tag)
    return tags #tags contains a list of all tags whose instructions was provided in the instructions.csv file




def clear(log_file, valid_epcs):
    log_file = log_file.iloc[5:] #removes first 4 lines of each log file which contains reader machine's data
    #####################################
    for i, row in log_file.iterrows():
        if row['EPCValue'] not in valid_epcs: #removes the row if the tag is not present in the instructions.csv file
            log_file.drop(index = i, inplace = True)
        ##################################### drop unnecessary columns
        #####################################

    return log_file





def plot(log, valid_epcs, name, tags): # plots all the files in a single log file
    print(name)


    font = FontProperties()
    font.set_family('serif')
    font.set_name('Times')
    plt.yticks(fontname="Times", fontsize="15")
    plt.xticks(fontname="Times", fontsize="15")
    plt.legend(prop={'family': 'Times'})

    for epc in valid_epcs:
        this_epc_traces = log.loc[log['EPCValue'] == str(epc)] #returns the specific epc that is required to plot
        if this_epc_traces.empty == False:

            times = this_epc_traces['TimeStamp'].tolist()
            RSSIs = this_epc_traces['RSSI'].tolist()
            for i in range(0, len(times)):
                times[i] = float(times[i])
                RSSIs[i] = int(RSSIs[i])

                ########problematic color
            color = ""
            for tag in tags:
                if tag.get_epc() == epc:
                    color = tag.get_color()
                ##############problematic color
            #(color)
            plt.scatter(times, RSSIs, label= epc, marker='o', color= color ) #plot the graph



    plt.grid(b=True, which='major', color='#666666', linestyle=':')
    plt.ylabel('RSS (dBm)', fontfamily="Times", fontsize="18")
    plt.xlabel('Time', fontfamily="Times", fontsize="18")
    plt.legend()
    plt.savefig('./rfid_logs/'+str(name)+"/"+str(name)+".png", dpi = 500) #saves the file into the directories of the log files
    plt.clf()

def plot_graph(log_name, tags, unit, x_offset, y_offset):
    #find the location
    [y, x] = log_name.split('_')
    x = int(x) * unit
    y = int(y) * unit
    ###################################
    img = cv2.imread('figure.png')
    red = [233, 66, 245]
    cv2.circle(img, (x_offset + x, y_offset + y), (10), red, thickness=19, lineType=8, shift=0)
    cv2.imwrite('./rfid_logs/'+str(log_name)+"/figure.png", img)


def make_html(directory, index):
    page_title = index
    doc = dominate.document(title=page_title)


    #test = div(data_employee='101011')
    #print(test)
    with doc.head:
        link(rel='stylesheet', href='style.css')
    doc.add(h1("Experiment name: "+str(page_title)+":"))

    with os.scandir(str(directory)) as gesture_directories:

        for gesture_directory in gesture_directories:
            if os.path.isdir(gesture_directory):

                log_name = str(gesture_directory.name)
                [y, x] = log_name.split('_')
                d = div(cls='plot')
                d.add(h3("location of touch is at: x="+str(x)+" y="+str(y)))


                p = img(src="rfid_logs/"+str(log_name)+"/figure.png", figcaption = "setup")
                d.add(p)

                p = img(src="rfid_logs/" + str(log_name)+"/" + str(log_name)+".png", figcaption = "RSS of the tags")
                d.add(p)

                doc.add(d)
    #print(str(doc))


    f = open(str(page_title) + ".html", "w")
    f.write(str(doc))
    f.close()


if __name__ == "__main__":

    tags = read_tags (sys.argv[2])
    log_files = []
    log_files = read_gestures(sys.argv[1])  # read sheets from directories
    ########################################finds all valid epcs
    valid_epcs = []
    for tag in tags:
        valid_epcs.append(tag.get_epc())
    ########################################
    for log_file in log_files:
        log_name = log_file.name #there is a bug that log file names mess up after clearing them
        log_file = clear(log_file, valid_epcs)#clear tags and just keep needed ones based on instructions.csv
        plot(log_file, valid_epcs, log_name, tags)#plots the log files
        unit = 75 # unit of pixels
        plot_graph(log_name, tags, unit, 160,265)
    ########################################
    make_html(sys.argv[1], sys.argv[3])



