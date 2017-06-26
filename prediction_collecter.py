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

	def __init__(self, routes=['J'], run_interval_sec=60, max_runs=60 * 24 * 2):
		self.run_count = 0
		self.max_runs = max_runs
		self.run_interval_sec = run_interval_sec
		self.stop_list = stop_loader.collect_stops(routes, False)
		self.url = xml_reader.multi_predictions_url(self.stop_list)
		self.predictions = pd.DataFrame()
		if os.path.isfile(self.fname()):
			self.predictions = pd.read_pickle(self.fname())

	def fname(self):
		cur_time = time_now()
		return 'predictions_{}-{}.pkl'.format(cur_time.day, cur_time.month)

	def run(self):
		self.run_count += 1
		if self.run_count > self.max_runs:
			return
		threading.Timer(self.run_interval_sec, self.run).start()
		self.get_stop_predictions()

	def get_stop_predictions(self):
		prediction_results = xml_reader.read_xml(self.url)
		timestamp = time_now()
		pred_list = []
		for stop in prediction_results['predictions']:
			stop_data = get_xml_tags(stop)
			if 'direction' in stop:
				dir_all = stop['direction']
				dir_data = get_xml_tags(dir_all)
				for pred in dir_all['prediction']:
					if isinstance(pred, dict):
						pred_data = get_xml_tags(pred)
						pred_data.update(dir_data)
						pred_data.update(stop_data)
						pred_data['timestamp'] = timestamp
						pred_list.append(pred_data)

		predictions = pd.DataFrame(pred_list)

		if not os.path.isfile(self.fname()):
			self.predictions = self.predictions[0:0]

		self.predictions = self.predictions.append(predictions, ignore_index=True)

		self.predictions.to_pickle(self.fname())

if __name__ == '__main__':
	p = PredictionCollecter()
	p.run()
