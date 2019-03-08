#!/usr/bin/env python3

from geographiclib.geodesic import Geodesic
from array import *
import math
import sys
import os
import csv
import copy
import map_plotting

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
        # import ipdb; ipdb.set_trace()
        init_list = []
        first_data = False
        init_timestamp = 0
        last_timestamp = 0
        for line in data:
            timestamp = line['time_stamp']
            last_timestamp = timestamp
            if first_data == False:
                init_timestamp = timestamp
                first_data = True
            if timestamp == init_timestamp:
                init_list.append(line)
    return (init_list, init_timestamp, last_timestamp)


def update_data(csv_file, prev_timestamp, time_interval):#time_interval is in seconds 
    with open(csv_file, "r") as read_file:
        data = csv.DictReader(read_file)
        updated_prev_timestamp = 0
        # found__updated_prev_timestamp = False
        updated_list = []
        for line in data:
            timestamp = line['time_stamp']
            updated_prev_timestamp = timestamp
            if int(timestamp) <= int(prev_timestamp) + int(time_interval) - 120: #time_interval is in seconds 
                continue
            elif int(timestamp) > int(prev_timestamp) + int(time_interval) - 120 and int(timestamp) <= int(prev_timestamp) + int(time_interval) + 120:
                updated_list.append(line) 
            else:
                break
    return (updated_list, updated_prev_timestamp)



def build_grid_count(points, init_list):
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
                    # print("Inserted {} ({}, {}) in ({}, {})".format(item['id'], item['latitude'], item['longitude'], cluster_count-i-1, j))
                    found = True
                    break
            if found:
                break
        if not found:
            print("Item {} is out of range ({}, {})".format(item['id'], item['latitude'], item['longitude']))

    return grid_count


def analyze_activity(freq_grid, prev_count, updated_count):
    for line in range(len(updated_count)):
        for item in range(len(updated_count[line])):
            # import ipdb; ipdb.set_trace()
            if len(updated_count[line][item]) == len(prev_count[line][item]):
                prev_battery_level = 0
                updated_battery_level = 0
                for each in updated_count[line][item]:
                    updated_battery_level += int(each['battery_level'])
                for each in prev_count[line][item]:
                    prev_battery_level += int(each['battery_level'])
                if abs(updated_battery_level - prev_battery_level) <= 2:
                    continue
                else:
                    freq_grid[line][item] += int(abs(updated_battery_level - prev_battery_level)/2)
            else:
                # import ipdb; ipdb.set_trace()
                freq_grid[line][item] += abs(len(prev_count[line][item]) - len(updated_count[line][item]))
    return freq_grid



def format_grid(grid):
    for line in grid:
        for line2 in line:
            print(len(line2), end=' ')
        print("\n")
    print("\n")


def concat_rows(rows):
    final_list = []
    for row in rows:
        final_list = final_list + row
    return final_list

def main(analysis_type):
    geod = Geodesic.WGS84  # define the WGS84 ellipsoid
    # An over estimation
    if analysis_type == "under":
        origin = geod.Direct(34.413112, -119.855395, 225, 1.2e3)
        x_end = geod.Direct(origin['lat2'], origin['lon2'], 90, 1.69e3)
        y_end = geod.Direct(origin['lat2'], origin['lon2'], 0, 1.69e3)
        #format_result(origin, x_end, y_end)
        points = divide(origin, x_end, y_end, 0) #to get the under-estimated grid

    elif analysis_type == "over":
        origin = geod.Direct(34.413112, -119.855395, 225, 1.69e3)
        x_end = geod.Direct(origin['lat2'], origin['lon2'], 90, 2.4e3)
        y_end = geod.Direct(origin['lat2'], origin['lon2'], 0, 2.4e3)
        #format_result(origin, x_end, y_end)
        points = divide(origin, x_end, y_end, 120) #to get the over-estimated grid
        print(points)
        output_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "daily_csvs/2019_02_19.csv")
        (init_list, init_timestamp, last_timestamp) = intialize_data(output_dir) #to get the first available data of each day(using 02/18)
        print(len(init_list))
        init_count = build_grid_count(points, init_list)#to initialze the count of each area
        print("The initial board is")
        format_grid(init_count) 
        # print(last_timestamp)
        res_list = [] #to hold all the results
        updated_grid = [] #to hold all the counts in each grid
        freq_grid = [[0 for i in range(len(init_count))] for j in range(len(init_count))]
        
        current_timestamp = init_timestamp
        prev_count = init_count
        

        while int(current_timestamp) < int(last_timestamp):
            (updated_list,current_timestamp) = update_data(output_dir, current_timestamp, 36000) #to get an updated grid
            res_list.append(updated_list)
            updated_count = build_grid_count(points, updated_list)#to update the count grid
            # print(updated_count)
            print("The updated board is")
            format_grid(updated_count)
            
            # compare with the previous grid counts
            # import ipdb; ipdb.set_trace()
            freq_grid = analyze_activity(freq_grid, prev_count, updated_count)
            prev_count = updated_count
            # format_grid(updated_count)# to print out the grid 
            # updated_grid.append(updated_count)
            # format_grid(updated_count)
        # print(len(res_list))
        # print(len(updated_grid))
        # print(len(freq_grid))
        print(freq_grid)
        # format_grid(updated_grid)
        # print(updated_count)
        # print(resList)
        # print(init_timestamp)
        # print(current_timestamp)
        # import ipdb; ipdb.set_trace()
       
        # format_grid(updated_count)
        # print(time)




        ##############Start Plotting##############
        base_map = map_plotting.Mapping()
        final_list = concat_rows(freq_grid)
        base_map.generate_grid_plot(20, final_list, 0.5, True)


    
    else:
        print("Analysis type {} not recognized!".format(analysis_type))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        sys.exit(0)
    else:
        main(sys.argv[1])