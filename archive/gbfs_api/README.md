Script to fetch data from https://mds.bird.co/gbfs

## Usage

` python fetch_scooter_datay.py`

## Configuration options

* `FETCH_URL` - Api End point for `GET` request. Currently fetches data for Los Angeles from `"https://mds.bird.co/gbfs/los-angeles/free_bikes"`
* `DATA_DIR` - Path to save the data. Script creates folders by dates and creates json files timestamped e.g `12345678.json`
* `SLEEP_TIME` - Make next request after x seconds
* `end_val` - Number of requests made