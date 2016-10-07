import threading
import stop_loader
import xml_reader
from datetime import datetime
from pytz import timezone    
import argparse

def get_stop_predictions():
	threading.Timer(60.0, get_stop_predictions).start()
	url = xml_reader.multi_predictions_url(stop_list)
	raw_predictions = xml_reader.get_raw_xml(url)

	pacific_time = timezone('US/Pacific')
	pa_time = datetime.now(pacific_time)
	formatted_time = pa_time.strftime('%Y-%m-%d_%H:%M:%S')

	with open('predictions.txt','a') as f:
		f.write(formatted_time + '\n')
		f.write(str(raw_predictions) + '\n')

def get_routes():
	url = xml_reader.routes_list_url()
	routes_xml_dict = xml_reader.read_xml(url)
	raw_routes_list = routes_xml_dict['route']
	routes_list = [r['@tag'] for r in raw_routes_list]
	return routes_list
  

parser = argparse.ArgumentParser(description='Get muni predictions')
parser.add_argument('--list', metavar='r', type=str, nargs='+',
                   help='choose specific routes (default: all routes)')
args = parser.parse_args()

if args.list == None:
	stop_list = stop_loader.collect_stops(get_routes(),sample=True)
else:
	print(args.list)
	stop_list = stop_loader.collect_stops(args.list,sample=False)

get_stop_predictions()