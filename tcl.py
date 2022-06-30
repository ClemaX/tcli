#!/usr/bin/env python

import requests
from urllib.parse import urlencode
from json import loads
from datetime import datetime

API_ROUTES = 'https://carte.tcl.fr/api'
API_PLACES = 'https://www.tcl.fr/api'

REFERER_SEARCH = 'https://www.tcl.fr/'
REFERER_ITINERARY = 'https://carte.tcl.fr/route-calculation'

DEFAULT_PARAMS = 'departure,metro,funiculaire,tramway,bus,bss'

DATETIME_FMT = '%Y%m%dT%H%M%S'


def places_search(term, filter_type='all'):
	headers = {
		'Referer': REFERER_SEARCH,
		'X-Requested-With': 'XMLHttpRequest',
	}

	params = {
		'q': term,
	}

	url = f'{API_PLACES}/navitia/search-places'

	response = requests.get(url, params=params, headers=headers)

	results = loads(response.content)

	if filter_type != "all":
		results = filter(lambda r: r['type'] == filter_type, results)

	return results


def places_print(places):
	for place in places:
		type = place['type']
		name = place['label']
		id = place['id']

		print(f'{type} - {name}: {id}')


def itinerary(stop_from, stop_to):
	when = 'now'
	filters = 'departure,metro,funiculaire,tramway,bus,bss'

	headers = {'Referer': REFERER_ITINERARY}
	params = {
		'datetime': when,
		'from': stop_from,
		'to': stop_to,
		'params': filters,
	}

	url = f'{API_ROUTES}/itinerary'

	response = requests.get(url, params=params, headers=headers)

	itinerary = loads(response.content)

	for j in itinerary["journeys"]:
		departure = datetime.strptime(j["departure_date_time"], DATETIME_FMT)
		arrival = datetime.strptime(j["arrival_date_time"], DATETIME_FMT)
		print(f'{departure.time()} - {arrival.time()}')


campus = list(places_search("campus region numerique", "stop_area"))[0]
home = list(places_search("mermoz pinel", "stop_area"))[0]

places_print([campus, home])

itinerary(home['id'], campus['id'])
