#!/usr/bin/env python3

import csv
import json
import os
import datetime

INPUT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data_dump")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "csv_output.csv")

def parse_filename_to_timestamp(filename):
    year, month, date, hour, minute, second = filename[0:4], filename[4:6], \
                                               filename[6:8], filename[9:11], \
                                               filename[11:13], filename[13:15]
    
    time_stamp = datetime.datetime(*[int(x) for x in [year, month, date, hour, minute, second]])
    return int(time_stamp.timestamp())

def main():
    with open(OUTPUT_DIR, "w") as write_file:
        csv_writer = csv.writer(write_file)
        csv_writer.writerow(['id', 'latitude', 'longitude', 'battery_level', 'captive', 'time_stamp'])
        for dump in os.listdir(INPUT_DIR):
            try:
                if not dump.startswith('output'): 
                    with open(INPUT_DIR + "/" + dump, "r") as read_file:
                        data = read_file.readlines()
                        output = json.loads(data[1])

                        for item in output['birds']:
                            csv_writer.writerow([
                                item['id'], 
                                item['location']['latitude'], 
                                item['location']['longitude'],
                                item['battery_level'],
                                item['captive'],
                                parse_filename_to_timestamp(dump)
                            ])
            except json.decoder.JSONDecodeError:
                print("File {} malformed!!".format(dump))
                continue
                        
if __name__ == "__main__":
    main()
