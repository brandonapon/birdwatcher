#!/usr/bin/env python3

from bird_api import BirdWatcher

birdwatcher = BirdWatcher()
birdwatcher.update_login_info()
print(birdwatcher.email, birdwatcher.guid)
birdwatcher.login()
birdwatcher.set_search(34.413112,-119.855395, 10, 1200)
output = birdwatcher.pull_data()
birdwatcher.export_to_file_weekend('this input doesnt do anything', output)
# b.pull_data()
