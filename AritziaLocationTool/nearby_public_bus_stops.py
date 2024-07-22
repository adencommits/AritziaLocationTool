import googlemaps


def analyze_location_factors(latitude, longitude, api_key):
    """
    Analyze location factors using Google Maps data
    :param latitude:
    :param longitude:
    :param api_key:
    :return:
    """
    # Initialize Google Maps client with API key
    gmaps = googlemaps.Client(key=api_key)

    # Find nearby public transit stops using Google Places API
    public_transit_stops = set()
    places_result_transit = gmaps.places_nearby(location=(latitude, longitude), radius=1700, type='bus_station')

    if 'results' in places_result_transit:
        for place in places_result_transit['results']:
            # Calculate distance from input coordinates to each bus stop
            distance_result = gmaps.distance_matrix(origins=(latitude, longitude), destinations=place['geometry']['location'], mode='walking')
            distance = distance_result['rows'][0]['elements'][0]['distance']['text']
            public_transit_stops.add((place['name'], distance))

    return list(public_transit_stops)


latitude = '43.67029848772484'
longitude = '-79.43515535336972'

print(analyze_location_factors(latitude, longitude, api_key='AIzaSyAEVMMBIjhk05WmXezmIlrBlg7IuhT3vzg'))