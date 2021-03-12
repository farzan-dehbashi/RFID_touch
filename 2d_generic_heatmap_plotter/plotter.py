

import os
import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns

def create_tag_csv_file(width):
    columns = []
    for x in range(0,width+1):
        columns.append(str(x))
    df = pd.DataFrame(columns=columns)
    return df

if __name__ == "__main__":
    #input parameters
    width = 5
    height = 5
    input_path = 'input_logs'
    tags = ['0x1111','0x2222','0x3333','0x4444']
    freq = '916.750'
    output = 'parsed_logs'
for tag in tags:
    result_df = create_tag_csv_file(width) # contains an initial instance of the specific tag array csv file to store averages of that tag on it
    for y in range(0,width+1):
        for x in range(0,height+1):

            trials =  os.listdir(input_path)
            trial_name = str(x)+"_"+str(y)+".csv"
            if trial_name in trials: #file name exists in results
                df = pd.read_csv(str(input_path)+"/"+trial_name, names = ["EPCValue", "TimeStamp", "RunNum", "RSSI", "Reader", "Frequency", "Power", "Antenna"])
                filt = (df['EPCValue'] == tag) & (df['Frequency'] == freq)
                filtered_df = df.loc[filt]
                RSSIs = filtered_df['RSSI']
                RSSIs = pd.to_numeric(RSSIs)
                average = RSSIs.mean()

                result_df.at[y,str(x)] = average
                print(str(x)+ " " +str(y)+ str(average))


    result_df.to_csv(str(output)+"/"+str(tag)+".csv")
    print(result_df.to_string())

    #nan_cells = result_df.at[8,8]
    #plt.figure(figsize=(1, 10))
    #sns.set_context('paper', font_scale=1.4)
    #sns.heatmap(result_df, annot=True, cmap='viridis')



