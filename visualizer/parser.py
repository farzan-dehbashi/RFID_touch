import pandas as pd
import sys
import os
class tag:
    def __init__(self, color):
        self.color = color
def Read(list_of_gestures):
    data_directory = sys.argv[1]
    with os.scandir("./"+str(data_directory)) as gesture_directories:
        for gesture_directory in gesture_directories:
            if os.path.isdir("./"+str(data_directory)+str(gesture_directory.name)):
                with os.scandir("./"+str(data_directory)+str(gesture_directory.name)) as gesture_files:
                    for gesture_file in gesture_files:
                        gesture_data = pd.read_csv(str(data_directory)+str(gesture_directory.name)+"/"+str(gesture_file.name))
                        gesture_data.name = str(gesture_file.name)
                        list_of_gestures.append(gesture_data)



            #with os.scandir("./"+str(data_directory)+str(gesture_directory.name)) as entries: #scanning the path
            #    for entry in entries:
            #        if entry.is_file():
            #            print("scanning file " + str(entry.name))
            #            gesture_data = pd.read_csv(str(data_directory)+str(gesture_directory)+str(entry.name))
            #            return gesture_data
def make_tags:
    instruction_sheet = pd.read_csv("instructions.csv")

def main():
    gesture_sheets = []
    Read(gesture_sheets)
    make_tags()


    for gesture in gesture_sheets:
        print(gesture.name)




if __name__ == "__main__":
    main()
