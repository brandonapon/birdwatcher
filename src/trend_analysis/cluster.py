import sys
import pandas as pd
import matplotlib as mpl
import datetime
import time
import numpy as np
import map_plotting
import os
from sklearn.cluster import KMeans

mpl.use('TkAgg')
from mapsplotlib import mapsplot as mplt
mplt.register_api_key('AIzaSyBmjHKY0e0z090bBg4-qXFpKW4XbdBr2RM')

def cluster(date, time_start, time_end, num_clusters):
	file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../api/bird_unofficial_api/csv_output.csv")
	df = pd.read_csv(file_path)

	df['datetime'] = df['time_stamp'].apply(lambda x: datetime.datetime.fromtimestamp(x))
	df['date_string'] = df['datetime'].apply(lambda x: x.strftime('%Y-%m-%d'))

	date = date.split('-')
	time_start = time_start.split(':')
	time_end = time_end.split(':')
	a = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time_start[0]), int(time_start[1])) # a = datetime.datetime(2019,2,13,8)
	b = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time_end[0]), int(time_end[1])) # b = datetime.datetime(2019,2,13,8,10)
	a_ts = int(time.mktime(a.timetuple()))
	b_ts = int(time.mktime(b.timetuple()))

	day_df = df[(df['time_stamp'] >= a_ts) & (df['time_stamp'] <= b_ts)]
	day_df = day_df.sort_values(by=['time_stamp'], ascending=True)
	
	data_arr = []
	for index, row in day_df.iterrows():
		data_arr.append({'id':row['id'],'lat':row['latitude'],'long':row['longitude']})

	lat_long = [[item['lat'],item['long']] for item in data_arr]
	X = np.array(lat_long)

	kmeans = KMeans(n_clusters=int(num_clusters)).fit(X)

	colors = ['blue','red','orange','green','purple']
	cluster_dict = {'latitude':[],'longitude':[],'color':[]}
	for i in range(len(data_arr)):
		point_color = colors[kmeans.labels_[i]]
		point_lat = data_arr[i]['lat']
		point_long = data_arr[i]['long']
		cluster_dict['latitude'].append(point_lat)
		cluster_dict['longitude'].append(point_long)
		cluster_dict['color'].append(point_color)

	cluster_df = pd.DataFrame.from_dict(cluster_dict)
	# mplt.plot_markers(cluster_df)
	return cluster_dict

if __name__ == "__main__":
	date = sys.argv[1]
	time_start = sys.argv[2]
	time_end = sys.argv[3]
	num_clusters = sys.argv[4]

	cluster_dict = cluster(date, time_start, time_end, num_clusters)
	mp = map_plotting.Mapping()
	mp.generate_cluster_plot(cluster_dict)
