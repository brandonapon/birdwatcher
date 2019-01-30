import sched
import datetime, time

class Scheduler:
    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def setup(self, interval, action, actionargs=()):
        self.scheduler.enter(interval, 1, self.setup, (interval, action, actionargs))
        action(*actionargs)
        print('executed')

    def run(self):
        self.scheduler.run()
