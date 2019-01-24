#!/usr/bin/env python3

import requests
import json
import os
from time import sleep
from datetime import datetime


s = requests.Session()
FETCH_URL = "https://mds.bird.co/gbfs/los-angeles/free_bikes"
LAST_UPDATED = None
DATA_DIR = '/home/pi/Desktop/git/birdwatcher/archive/gbfs_api/'
SLEEP_TIME = 5 #in seconds
TODAY = datetime.today().strftime('%Y-%m-%d')
DL_PATH = DATA_DIR+TODAY
if not os.path.exists(DL_PATH):
    os.mkdir(DL_PATH)
    print('Created directory for '+TODAY)

counter = 0
end_val = 1
while(counter < end_val):
    r = s.get(FETCH_URL)
    json_data = r.json()
    last_update_ts = json_data['last_updated']
    if(LAST_UPDATED is None or LAST_UPDATED < last_update_ts):
        path = DL_PATH+'/'+str(last_update_ts)+'.json'
        f = open(path,'w')
        json.dump(json_data, f)
        f.close()
        counter += 1
        print('Fetched '+str(counter)+' files successfully..')
        sleep(SLEEP_TIME) #Sleep x minutes after every file fetch
        #Parsing date from timestamp file name -> datetime.fromtimestamp(ts)
print("Data fetching complete.")
