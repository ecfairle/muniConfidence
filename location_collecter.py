import threading
import stop_loader
import xml_reader
import sys
from datetime import datetime
from pytz import timezone
import pandas as pd
import os

def get_xml_tags(d):
	return {k.replace('@', '') : v for k,v in d.items() if k.startswith('@')}

def time_now():
	pacific_time = timezone('US/Pacific')
	pa_time = datetime.now(pacific_time)
	# formatted_time = pa_time.strftime('%Y-%m-%d_%H:%M:%S')
	return pa_time

class PredictionCollecter(object):

	def __init__(self, route='J', run_interval_sec=20, max_runs=3 * 60 * 24 * 2):
		self.run_count = 0
		self.max_runs = max_runs
		self.run_interval_sec = run_interval_sec
		self.locations = pd.DataFrame()
		self.url = xml_reader.vehicle_locations_url('J')
		if os.path.isfile(self.fname()):
			self.locations = pd.read_pickle(self.fname())

	def fname(self):
		cur_time = time_now()
		return 'locations_{}-{}.pkl'.format(cur_time.month, cur_time.day)

	def run(self):
		self.run_count += 1
		if self.run_count > self.max_runs:
			return
		threading.Timer(self.run_interval_sec, self.run).start()
		self.get_vehicle_locations()

	def get_vehicle_locations(self):
		locations_raw = xml_reader.read_xml(self.url)
		timestamp = time_now()
		loc_list = []
		for tag, stop_data in locations_raw.items():
			if tag == 'vehicle':
				for stop in stop_data:
					loc_data = get_xml_tags(stop)
					loc_list.append(loc_data)


		locations = pd.DataFrame(loc_list)

		if not os.path.isfile(self.fname()):
			self.locations = self.locations[0:0]

		self.locations = self.locations.append(loc_list, ignore_index=True)
		print (self.locations.tail())

		self.locations.to_pickle(self.fname())

if __name__ == '__main__':
	p = PredictionCollecter()
	p.run()
