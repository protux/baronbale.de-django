from django.http import HttpResponse
from django.shortcuts import render

import json, urllib3
import calendar 
from datetime import datetime

DOMAIN = "https://grobbo.de"
PORT_KITCHEN = "9996"
PORT_LIVING_ROOM = "9995"
DATETIMEFORMAT = "%d.%m.%Y %H:%M %z"

def index(request):
	humidity = fetch_json(temp=False)
	temp = fetch_json(humidity=False)
	return render(request, 'lab/index.html', {'data_humidity_liv': humidity['Wohnzimmer']['data'], 'data_humidity_kit': humidity['K\udcc3che']['data'], 'data_temperature_liv': temp['Wohnzimmer']['data'], 'data_temperature_kit': temp['K\udcc3che']['data']})
	#return render(request, 'lab/index.html', {'data_humidity': humidity, 'data_temperature': temp['Wohnzimmer']['data']})
def display_json(request):
	json_dict = fetch_json(humidity=False)
	return HttpResponse(json.dumps(json_dict))
	
def fetch_json(temp=True, humidity=True):
	http = urllib3.PoolManager()
	server_request = http.request('GET', '{}:{}'.format(DOMAIN, PORT_LIVING_ROOM))
	json_dict = json.loads(server_request.data)
	server_request = http.request('GET', '{}:{}'.format(DOMAIN, PORT_KITCHEN))
	json_dict.update(json.loads(server_request.data.decode('utf-8', 'replace')))
	if not temp:
		return strip_temperature(json_dict)
	if not humidity:
		return strip_humidity(json_dict)
	return json_dict
	
def strip_temperature(json_dict):
	return strip_from_index(json_dict, 2)
	
def strip_humidity(json_dict):
	return strip_from_index(json_dict, 1)

def strip_from_index(json_dict, index):
	new_dict = {}
	for key, value in json_dict.items():
		value_list = []
		for dataset in value:
			date = datetime.strptime(dataset[0], DATETIMEFORMAT)
			plot_date = calendar.timegm(date.timetuple()) * 1000 + 3600000
			value_list += [[plot_date, dataset[index]]]
		new_dict[key] = {'label': key, 'data': value_list[-144:]} 
	return new_dict
	
