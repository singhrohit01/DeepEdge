
import datetime

class Timer:

    def __init__(self):
        super().__init__()
        self._start_time = None
        self._end_time = None

    def start(self):
        self._start_time = self.get_current_time()
        return self

    def stop(self):
        self._end_time = self.get_current_time()
        return self

    def start_time(self):
        return self.format_time(self._start_time)
    
    def end_time(self):
        return self.format_time(self._end_time)

    def diff(self):
        return (self._end_time - self._start_time).total_seconds()

    def get_current_time(self):
        return datetime.datetime.now()

    def format_time(self, time):
        return time.strftime('%Y-%m-%d %H:%M:%S')