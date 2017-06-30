import xmltodict
import urllib
import sys

NEXTBUS_BASE_URI = 'http://webservices.nextbus.com/service/publicXMLFeed?'
AGENCY = 'sf-muni'

def read_xml(url):
	xml_data = get_raw_xml(url)

	dict = xmltodict.parse(xml_data)['body']
	if 'Error' in dict:
		print('XML Retrieval Error')
		sys.exit()
	return dict

def get_raw_xml(url):
	req = urllib.request.Request(url, headers={'User-Agent' : 'Magic Browser'})
	con = urllib.request.urlopen(req)

	data = con.read()
	con.close()
	return data


def stop_list_url(route):
	return '{}command=routeConfig&a={}&r={}&terse'.format(NEXTBUS_BASE_URI, AGENCY, route)

def routes_list_url():
	return '{}command=routeList&a={}'.format(NEXTBUS_BASE_URI, AGENCY)

def vehicle_locations_url(route):
	loc_url = '{}command=vehicleLocations&a={}&r={}&t=0'
	return loc_url.format(NEXTBUS_BASE_URI,AGENCY,route)

def multi_predictions_url(stop_list):
	pred_template = '{}command=predictionsForMultiStops&a={}{}'
	stop_strs = ['&stops={}|{}'.format(route['route'],stop) for route in stop_list for stop in route['stops']]
	return pred_template.format(NEXTBUS_BASE_URI,AGENCY,''.join(stop_strs))
