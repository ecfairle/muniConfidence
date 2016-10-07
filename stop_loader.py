import sys
import xml_reader
import random

def collect_stops(routes, sample):
	stops = []
	random.seed(1)
	for route in routes:
		stops.append({'route':route,'stops': get_stop_list(route,sample)})

	return stops


def get_stop_list(route, sample=False):
	url = xml_reader.stop_list_url(route)
	stops_xml_dict = xml_reader.read_xml(url)

	raw_stop_list = stops_xml_dict['route']['stop']
	stop_list = [s['@tag'] for s in raw_stop_list]

	if sample:
		stop_list = random.sample(stop_list,5)

	return stop_list