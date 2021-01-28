import pandas as pd
import sys
import os

def Read(list_of_gestures):
    data_directory = sys.argv[1]
    with os.scandir("./"+str(data_directory)) as gesture_directories:
        for gesture_directory in gesture_directories:
            if os.path.isdir("./"+str(data_directory)+str(gesture_directory.name)):
                with os.scandir("./"+str(data_directory)+str(gesture_directory.name)) as gesture_logs:
                    for gesture_log in gesture_logs:
                        list_of_gestures.append(gesture_log)



            #with os.scandir("./"+str(data_directory)+str(gesture_directory.name)) as entries: #scanning the path
            #    for entry in entries:
            #        if entry.is_file():
            #            print("scanning file " + str(entry.name))
            #            gesture_data = pd.read_csv(str(data_directory)+str(gesture_directory)+str(entry.name))
            #            return gesture_data



def main():
    gestures = []
    Read(gestures)
    for gesture in gestures:
        print(gesture.to_string())




if __name__ == "__main__":
    main()
