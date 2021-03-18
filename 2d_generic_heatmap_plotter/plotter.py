import os
import pandas as pd
import argparse
import seaborn as sns
import matplotlib.pyplot as plt
import shutil

def create_df(width):
    columns = []
    for x in range(0, width):
        columns.append(str(x))
    df = pd.DataFrame(columns=columns)
    return df

def check_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def plot_heatmap(df, directory, file_name):

    #TODO: the save and load should be removed and the problem with the index of the sheet should be resolved
    df.to_csv("temp.csv")
    df = pd.read_csv('temp.csv', index_col=0) #index col 0 is needed for seaborn
    os.remove("temp.csv")
    # end of todo

    style = 'Blues'
    if args.style:
        style = args.style
    plt.figure(figsize=(7, 5))
    sns.set_context('paper', font_scale=1.4)
    heat_map = sns.heatmap(df, annot=True, cmap=style, fmt='.3g')
    heat_map.figure.savefig(str(directory)+"/"+str(file_name))

parser = argparse.ArgumentParser(description='configuration for the reader')
parser.add_argument('-w', '--width', type=int, metavar='', required=True, help='sets width of the pad in cm (if width is 3 cm, 0,1,2 will be shown)')
parser.add_argument('-H', '--height', type=int, metavar='', required=True, help='sets height of the pad in cm (if height is 3 cm, 0,1,2 will be shown)')
parser.add_argument('-i', '--input', type=str, metavar='', required=True, help='sets input directory')
parser.add_argument('-o', '--output', type=str, metavar='', required=True, help='sets output directory')
parser.add_argument('-f', '--frequency', type=str, metavar='', required=True, help='sets frequency to be filtered (like: 916.750)')
parser.add_argument('-s', '--printstd', action= 'store_true', required=False, help='prints std dataframe')
parser.add_argument('-c', '--printcount', action= 'store_true', required=False, help='prints number of reads in that freq by that tag in that location dataframe')
parser.add_argument('-m', '--printmean', action= 'store_true',required=False, help='prints mean dataframe')
parser.add_argument('--style', type=str, metavar='', required=False, help='set the style of the seaborn heatmap e.g. viridis, Blues')
args = parser.parse_args()

#default input params
#TODO: make these flags:
width = args.width
height = args.height
input_dir = args.input
output_dir = args.output
tags = ['0x2d041111', '0x2d4300600322e1dd26000000', '0x2d4200600322e08ecd000000', '0x00e200600322e13181000000']
freq = args.frequency

for tag in tags:
    #making statistical dfs
    count_df = create_df(width)
    mean_df = create_df(width) # contains an initial instance of the specific tag array csv file to store averages of that tag on it
    std_df = create_df(width)
    # min, max 25% and 50% and 75% can be also added

    for y in range(0, height):
        for x in range(0, width):

            trials = os.listdir(input_dir)
            trial_name = str(x)+"_"+str(y)+".csv"
            if trial_name in trials:#file name exists in results
                df = pd.read_csv(str(input_dir)+"/"+trial_name, names=["EPCValue", "TimeStamp", "RunNum", "RSSI", "Reader", "Frequency", "Power", "Antenna"])
                filt = (df['EPCValue'] == tag) & (df['Frequency'] == freq)
                filtered_df = df.loc[filt]
                RSSIs = filtered_df['RSSI']
                RSSIs = pd.to_numeric(RSSIs)

                print(RSSIs)

                #making a df that contains a grid of all mean, std, count of each tag by different locations
                count_df.at[y,str(x)] = RSSIs.describe().loc['count']
                mean_df.at[y,str(x)] = RSSIs.describe().loc['mean']
                std_df.at[y,str(x)] = RSSIs.describe().loc['std']

    #prints results based on flags in terminal
    if args.printcount:
        print("count " + str(tag))
        print(count_df.to_string())
        check_dir(str(output_dir)+"/"+str(tag))
        mean_df.to_csv(str(output_dir) + "/" + str(tag) + "/" + str(tag) + "_count.csv")
        plot_heatmap(count_df, str(output_dir) + "/" + str(tag) , str(tag) + "_count")
        print("*********************")
    if args.printmean:
        print("mean " + str(tag))
        print(mean_df.to_string())
        check_dir(str(output_dir) + "/" + str(tag))
        mean_df.to_csv(str(output_dir) + "/" + str(tag) + "/" + str(tag) + "_mean.csv")
        plot_heatmap(mean_df, str(output_dir) + "/" + str(tag), str(tag) + "_mean")
        print("*********************")
    if args.printstd:
        print("std " + str(tag))
        print(std_df.to_string())
        check_dir(str(output_dir) + "/" + str(tag))
        mean_df.to_csv(str(output_dir) + "/" + str(tag) + "/" + str(tag) + "_std.csv")
        plot_heatmap(std_df, str(output_dir) + "/" + str(tag), str(tag) + "_std")
    print("##########################################")


