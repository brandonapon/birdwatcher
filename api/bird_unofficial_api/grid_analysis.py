#!/usr/bin/env python3

from geographiclib.geodesic import Geodesic
from array import *
import math
import sys
import os
import csv
import copy



def usage():
    print("grid_analysis.py <analysis_type>")

def format_result(origin, x_end, y_end):
    print("The origin is ({:.8f}, {:.8f}).".format(origin['lat2'], origin['lon2']))
    print("The x_end is ({:.8f}, {:.8f}).".format(x_end['lat2'], x_end['lon2']))
    print("The y_end is ({:.8f}, {:.8f}).".format(y_end['lat2'], y_end['lon2']))

def divide(origin, x_end, y_end, cluster_len):
    geod = Geodesic.WGS84  # define the WGS84 ellipsoid
    dist_x= geod.Inverse(origin['lat2'], origin['lon2'], x_end['lat2'], x_end['lon2'])
    #dist_y = geod.Inverse(origin['lat2'], origin['lon2'], y_end['lat2'], y_end['lon2'])
    # print(dist_x)
    print("The dist_x is {:.3f} m.".format(dist_x['s12']))
    # print("The dist_y is {:.3f} m.".format(dist_y['s12']))
    
    count = math.ceil(dist_x['s12'] / cluster_len)
    print(count)

    points = [None]*count
    
    for i in range(0,count):
        points[i] = [None]*count
        for j in range(0,count): 
           res = geod.Direct(origin['lat2'], origin['lon2'], 90, cluster_len*j)
           points[i][j] = (res['lat2'], res['lon2'])
        origin = geod.Direct(origin['lat2'], origin['lon2'], 0, cluster_len)

    return points



def intialize_data(csv_file):
    with open(csv_file, "r") as read_file:
        data = csv.DictReader(read_file)
        init_list = []
        for line in data:
            if line['id'] == 'id':
                continue
            timestamp = line['time_stamp']
            if timestamp == "1551441604":
                init_list.append(line)
    return init_list


def update_data(csv_file):
    with open(csv_file, "r") as read_file:
        data = csv.DictReader(read_file)
        updated_list = []
        for line in data:
            if line['id'] == 'id':
                continue
            timestamp = line['time_stamp']
            if timestamp > "1551441604" and timestamp <= "1551474004":
                updated_list.append(line)
    return updated_list



def initialize_count(points, init_list):
    cluster_count = len(points)-1
    grid_count = [[] for i in range(cluster_count)]
    for i in range(cluster_count):
        grid_count[i] = [[] for i in range(cluster_count)]

    for item in init_list:
        lat = float(item['latitude'])
        lon = float(item['longitude'])
        found = False
        for i in range(cluster_count):
            for j in range(cluster_count):
                if lat <= points[i][j][0] and lon <= points[i][j][1]:
                    grid_count[cluster_count-i-1][j].append(item)
                    print("Inserted {} ({}, {}) in ({}, {})".format(item['id'], item['latitude'], item['longitude'], cluster_count-i-1, j))
                    found = True
                    break
            if found:
                break
        if not found:
            print("Item {} is out of range ({}, {})".format(item['id'], item['latitude'], item['longitude']))

    return grid_count


def analyze_activity(init_count, updated_list):
    freq_grid = []
    for i in range(len(init_count)):
        freq_grid.append([])

    for item in updated_list:
        lat = float(item['latitude'])
        lon = float(item['longitude'])
        found = False




def format_grid(grid):
    for line in grid:
        for line2 in line:
            print(len(line2), end=' ')
        print("\n")


def main(analysis_type):
    geod = Geodesic.WGS84  # define the WGS84 ellipsoid
    # An over estimation
    if analysis_type == "under":
        origin = geod.Direct(34.413112, -119.855395, 225, 1.2e3)
        x_end = geod.Direct(origin['lat2'], origin['lon2'], 90, 1.69e3)
        y_end = geod.Direct(origin['lat2'], origin['lon2'], 0, 1.69e3)
        #format_result(origin, x_end, y_end)
        points = divide(origin, x_end, y_end, 0) #to get the over-estimated grid

    elif analysis_type == "over":
        origin = geod.Direct(34.413112, -119.855395, 225, 1.69e3)
        x_end = geod.Direct(origin['lat2'], origin['lon2'], 90, 2.4e3)
        y_end = geod.Direct(origin['lat2'], origin['lon2'], 0, 2.4e3)
        #format_result(origin, x_end, y_end)
        points = divide(origin, x_end, y_end, 600)
        print(points)
        output_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "csv_output.csv")
        init_list = intialize_data(output_dir) #to get the first available data of each day(using 03/01 4am now)
        print(len(init_list))
        init_count = initialize_count(points, init_list)#to initialze the count of each area
        format_grid(init_count) 
        updated_list = update_data(output_dir) #to get the data from the rest of the day
        #print(updated_list)
        

    
    else:
        print("Analysis type {} not recognized!".format(analysis_type))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        sys.exit(0)
    else:
        main(sys.argv[1])