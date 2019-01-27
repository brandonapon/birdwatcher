#!/usr/bin/env python3

'''
Contains code to utilize google maps for plotting of data.
refer to: https://github.com/tcassou/mapsplotlib for details on usage of package
'''
import matplotlib as mpl
mpl.use('TkAgg') # workaround for MacOS due to backend diff. Refer to comment on answer: https://stackoverflow.com/a/21789908
from mapsplotlib import mapsplot as mplt
import pandas as pd
import os
import sys

def main():
    # import CSV file
    name = sys.argv[1]
    INPUT_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "csv_output.csv")
    csv_file = open(INPUT_FILE, 'r')

    header_row = csv_file.readline()
    header_row = header_row[:-1] #remove "\n"
    headers = header_row.split(',')
    df = pd.read_csv(INPUT_FILE, usecols = headers, skiprows = [1])
    # print(df)

    # register api key
    mplt.register_api_key('AIzaSyBmjHKY0e0z090bBg4-qXFpKW4XbdBr2RM')

    mplt.density_plot(df['latitude'], df['longitude'])

if __name__ == "__main__":
    main()
