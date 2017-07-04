import sys
import xml_reader
import random

class MuniApi(object):

	NEXTBUS_BASE_URI = 'http://webservices.nextbus.com/service/publicXMLFeed?'
	AGENCY = 'sf-muni'
	loc_url = '{}command=vehicleLocations&a={}&r={{}}&t=0'.format(NEXTBUS_BASE_URI, AGENCY)
	stop_list_url = '{}command=routeConfig&a={}&r={{}}&terse'.format(NEXTBUS_BASE_URI, AGENCY)
	routes_list_url = '{}command=routeList&a={}'.format(NEXTBUS_BASE_URI, AGENCY)
	locations_url = '{}command=vehicleLocations&a={}&r={{}}&t=0'.format(NEXTBUS_BASE_URI, AGENCY)
	multi_predictions_url = '{}command=predictionsForMultiStops&a={}{{}}'.format(NEXTBUS_BASE_URI, AGENCY)

	def get_vehicle_locations(self, route):
		loc_url = self.locations_url.format(route)
		return xml_reader.read_xml(loc_url)

	def get_route_predictions(self, routes, sample=False):
		stop_list = self.collect_stops(routes, sample=sample)
		return self.get_stop_predictions(stop_list)

	def get_stop_predictions(self, stop_list):
		stop_strs = ['&stops={}|{}'.format(route['route'],stop) \
			for route in stop_list \
			for stop in route['stops']]
		url = self.multi_predictions_url.format(''.join(stop_strs))
		return xml_reader.read_xml(url)

	def collect_stops(self, routes, sample):
		stops = []
		random.seed(1)
		for route in routes:
			stops.append({'route':route,'stops': self.get_stop_list(route,sample)})

		return stops

	def get_stop_list(self, route, sample=False):
		url = xml_reader.stop_list_url(route)
		stops_xml_dict = xml_reader.read_xml(url)

		raw_stop_list = stops_xml_dict['route']['stop']
		stop_list = [s['@tag'] for s in raw_stop_list]

		if sample:
			stop_list = random.sample(stop_list,5)

		return stop_list
