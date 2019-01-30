import csv
import json
import os

INP_DIR = "/Users/vivekpradhan/Desktop/scooter_data/"

OUTPUT_CSV_FILE = "/Users/vivekpradhan/Desktop/output.csv"
csv_file = open(OUTPUT_CSV_FILE, mode='w')
csv_writer = csv.writer(csv_file)
#Headers
csv_writer.writerow(['id', 'latitude', 'longitude', 'battery_level', 'captive', 'time_stamp'])

#To convert timestamp to datetime object
#df['datetime'] = df['time_stamp'].apply(lambda x: datetime.fromtimestamp(x))

def write_json_to_csv(json_file):
    f = open(json_file)
    data = json.load(f)
    if('data' in data and 'bikes' in data['data']):
        for bike in data['data']['bikes']:
            def_bat_level = None
            captive = (bike['is_reserved'] == 1)
            file_ts = json_file.split('/')[-1].split('.')[0]
            csv_writer.writerow([bike['bike_id'], bike['lat'], bike['lon'], def_bat_level, captive, file_ts])
    f.close()

scooter_data = os.listdir(INP_DIR)
counter = 0
for item in scooter_data:
    if(item.startswith("2019")):
        dir_path = INP_DIR+item
        for json_file in os.listdir(dir_path):
            write_json_to_csv(dir_path+'/'+json_file)
            counter += 1
        print('Processed '+str(counter)+' json files')
csv_file.close()
print('Processing complete')