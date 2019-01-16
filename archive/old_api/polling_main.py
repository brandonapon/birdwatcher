from bird_api import BirdWatcher
from periodic_polling import Scheduler

poll_scheduler = Scheduler()

birdwatcher = BirdWatcher()
birdwatcher.update_login_info()
print(birdwatcher.email, birdwatcher.guid)
birdwatcher.login()
birdwatcher.set_search(34.413112,-119.855395, 10, 1200)
time_interval = 5
poll_scheduler.setup(time_interval, birdwatcher.export_to_file, ('output.txt', birdwatcher.pull_data()))
poll_scheduler.run()

# b.pull_data()