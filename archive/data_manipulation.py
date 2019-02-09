#!/usr/bin/env python3

import headers
import matplotlib as mpl
mpl.use('TkAgg') # workaround for MacOS due to backend diff. Refer to comment on answer: https://stackoverflow.com/a/21789908
import pandas as pd
import sys
import json
import csv
import datetime
import pytz

def init():
    headers.init()

# # parses int timestamp to month, day, hour, and min
# def timestamp_to_datetime(timestamp):
#     local_dt = datetime.fromtimestamp(timestamp)
#     return local_dt.month, local_dt.day, local_dt.hour, local_dt.min

# return full df of csv file
def csv_to_df():
    csv_file = open(headers.CSV_PATH, "r")
    header_row = csv_file.readline()
    header_row = header_row[:-1] #remove "\n"
    header = header_row.split(',')
    df = pd.read_csv(headers.CSV_PATH) #create Panda DF
    csv_file.close()
    days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    df['datetime'] = df['time_stamp'].apply(lambda x: datetime.datetime.fromtimestamp(x))
    df['date_string'] = df['datetime'].apply(lambda x: x.strftime('%Y-%m-%d'))
    df['week_day'] = df['datetime'].apply(lambda x: days[x.weekday()])
    # print(df.head())
    # print(df)
    return df

# returns dictionary of df partitioned by day
def partition_df_time(df, month, day):
    start_date = datetime.datetime(2019,month,day,0,0,0)
    print("start date: ", start_date)
    end_date = start_date + datetime.timedelta(days=1)
    print("end date: ", end_date)
    mask = (df['datetime'] > start_date) & (df['datetime'] < end_date)
    df_day = df.loc[mask]
    # df_day = df['time_stamp'].between(date, end_date, inclusive=False)
    # print (df_day)
    return df_day

def get_count_for_date(ds):
    day_df = df[df['date_string'] == ds]
    freq_df = day_df.groupby(pd.Grouper(key = 'datetime', freq='10min'))['id'].nunique()
    freq_df.plot(figsize=(10,5))

if __name__ == "__main__":
    init()
    df = csv_to_df()
    print(df['date_string'].unique())
    get_count_for_date('2019-02-05')

    # partition_df_time(df, 2, 6)
