from bird_api import bird_watch
from periodic_polling import periodic_scheduler

poll_scheduler = periodic_scheduler()

b = bird_watch()
b.update_login_info()
print(b.email, b.guid)
b.login()
b.set_search(34.413112,-119.855395, 10, 1200)
time_interval = 5
poll_scheduler.setup(time_interval, b.export_to_file, ('output.txt', b.pull_data()))
poll_scheduler.run()

# b.pull_data()
