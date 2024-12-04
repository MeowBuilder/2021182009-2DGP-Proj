import json
import os

class Clear_Time:
    def __init__(self):
        self.clear_times = []
        self.filename = 'records.json'
        self.load_times()

    def add_time(self, time_data):
        self.clear_times.append(time_data)
        self.clear_times.sort(key=lambda x: x['time'])
        self.save_times()

    def load_times(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.clear_times = json.load(f)
            except:
                self.clear_times = []
        else:
            self.clear_times = []

    def save_times(self):
        with open(self.filename, 'w') as f:
            json.dump(self.clear_times, f)

    def get_best_time(self):
        if len(self.clear_times) > 0:
            return self.clear_times[0]['time']
        return None

    def get_all_times(self):
        return self.clear_times

    def clear_records(self):
        self.clear_times = []
        self.save_times()