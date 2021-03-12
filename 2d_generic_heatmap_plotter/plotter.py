import os
import pandas as pd
import argparse

def create_tag_csv_file(width):
    columns = []
    for x in range(0, width):
        columns.append(str(x))
    df = pd.DataFrame(columns=columns)
    return df

parser = argparse.ArgumentParser(description='configuration for the reader')
parser.add_argument('-w', '--width', type=int, metavar='', required=True, help='sets width of the pad in cm (if width is 3 cm, 0,1,2 will be shown)')
parser.add_argument('-H', '--height', type=int, metavar='', required=True, help='sets height of the pad in cm (if height is 3 cm, 0,1,2 will be shown)')
parser.add_argument('-i', '--input', type=str, metavar='', required=True, help='sets input directory')
args = parser.parse_args()

#default input params
#TODO: make these flags:
width = args.width
height = args.height
input_path = args.input
tags = ['0x1111', '0x2222', '0x3333', '0x4444']
freq = '916.750'
output = 'parsed_logs'

for tag in tags:
    result_df = create_tag_csv_file(width) # contains an initial instance of the specific tag array csv file to store averages of that tag on it
    for y in range(0, height):
        for x in range(0, width):

            trials = os.listdir(input_path)
            trial_name = str(x)+"_"+str(y)+".csv"
            if trial_name in trials:#file name exists in results
                df = pd.read_csv(str(input_path)+"/"+trial_name, names=["EPCValue", "TimeStamp", "RunNum", "RSSI", "Reader", "Frequency", "Power", "Antenna"])
                filt = (df['EPCValue'] == tag) & (df['Frequency'] == freq)
                filtered_df = df.loc[filt]
                RSSIs = filtered_df['RSSI']
                RSSIs = pd.to_numeric(RSSIs)

                #TODO:calculate other statistics by flag
                average = RSSIs.mean()

                #TODO:plot timeline by flag
                result_df.at[y,str(x)] = average

    result_df.to_csv(str(output)+"/"+str(tag)+".csv")

    #TODO:add html maker
    print(result_df.to_string())
    print("#####################")
