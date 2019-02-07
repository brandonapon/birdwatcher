#!/usr/bin/env python3

import headers
import logging
import argparse
import pandas as pd
import matplotlib
import sys
import json
import csv

def init(debug_level):
    headers.init()
    # logging.basicConfig(filename='example.log',level=logging.DEBUG)

def parse_filename_to_timestamp(filename):
    year, month, date, hour, minute, second = filename[0:4], filename[4:6], \
                                               filename[6:8], filename[8:10], \
                                               filename[10:12], filename[12:14]

    time_stamp = datetime.datetime(*[int(x) for x in [year, month, date, hour, minute, second]])
    return int(time_stamp.timestamp())

# returns df for specific time period. note: "%Y%m%d-%H%M%S"
def csv_to_df(start, end):
    csv_file = open(headers.CSV_PATH, "r")
    header_row = csv_file.readline()
    header_row = header_row[:-1] #remove "\n"
    headers = header_row.split(',')
    df = pd.read_csv(headers.CSV_PATH, usecols = headers, skiprows = [1]) #create Panda DF
    csv_file.close()
    return df
    # print(df)

def __main__():
    csv_to_df(0,0)
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--verbosity", help="increase output verbosity")
    # args = parser.parse_args()
    # if args.verbosity:
    #     print("verbosity turned on")
