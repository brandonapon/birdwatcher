#!/usr/bin/env python3

"""
Question: Given the battery level, can we calculate how much Bird chargers are spending? Is this really a profitable side hustle?
"""	

import datetime
import pandas as pd
import matplotlib.pyplot as plt
def main():
	# df = pd.read_csv("/Users/saurabh/Desktop/work/birdwatcher/api/bird_unofficial_api/csv_output.csv")
	# # Preprocessing and adding date columns\n",
	# days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
	# df['datetime'] = df['time_stamp'].apply(lambda x: datetime.fromtimestamp(x))
	# df['date_string'] = df['datetime'].apply(lambda x: x.strftime('%Y-%m-%d'))
	# df['week_day'] = df['datetime'].apply(lambda x: days[x.weekday()])
	# print(df['week_day'])
	data = pd.read_csv("/Users/saurabh/Desktop/work/birdwatcher/api/bird_unofficial_api/csv_output.csv")
	





if __name__ == "__main__":
	main()