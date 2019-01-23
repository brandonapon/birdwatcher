Script to fetch data from https://mds.bird.co/gbfs

## Usage

` python fetch_scooter_datay.py`

## Configuration options

* `FETCH_URL` - Api End point for `GET` request. Currently fetches data for Los Angeles from `"https://mds.bird.co/gbfs/los-angeles/free_bikes"`
* `DATA_DIR` - Path to save the data. Script creates folders by dates and creates json files timestamped e.g `12345678.json`
* `SLEEP_TIME` - Make next request after x seconds
* `end_val` - Number of requests made

## Convert JSON files to CSV
` python process_json.py`

## Options

* `INP_DIR` - Directory where scooter data lives. Assumes the top level directory contains sub directories labelled by dates for eg. '2019-01-16' which would then contain individual json files named by their fetch timestamp i.e. `1547748050.json`
* `OUTPUT_CSV_FILE` - Path of CSV file to be output which would combine all the jsons into a single csv as per our defined schema
