import requests
from math import radians, sin, cos, sqrt, atan2
api_key = 'AIzaSyAEVMMBIjhk05WmXezmIlrBlg7IuhT3vzg'


def get_driving_duration(origin, destination, gmaps):
    """
    Get driving duration from origin to destination using Google Maps Directions API
    :param origin:
    :param destination:
    :param gmaps:
    :return:
    """
    try:
        # Calculate driving duration using Google Maps Directions API
        directions = gmaps.directions(origin, destination, mode='driving')
        print(directions)  # Print the full directions response
        if directions and 'legs' in directions[0] and 'duration' in directions[0]['legs'][0]:
            driving_time = directions[0]['legs'][0]['duration']['text']
            return driving_time
        else:
            return 'Driving time not available'
    except Exception as e:
        return f'Error calculating driving time: {str(e)}'


def get_nearest_place(latitude, longitude, place_type, api_key):
    """
    Get the nearest place of a specified type using Google Places API.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        place_type (str): Type of place to search for (e.g., 'hospital', 'fire_station', 'police').
        api_key (str): Your Google Places API key.

    Returns:
        dict: Information about the nearest place, including name, vicinity, location, and distance.
    """
    # Define Google Places API endpoint
    api_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    # Define API request parameters
    params = {
        "location": f"{latitude},{longitude}",
        "rankby": "distance",
        "type": place_type,
        "key": api_key
    }

    try:
        # Send API request to Google Places API
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an exception for bad responses

        # Parse JSON response
        data = response.json()

        # Extract information about the nearest place
        if "results" in data and data["results"]:
            nearest_place = data["results"][0]  # Get the first result (nearest place)

            # Calculate distance using Haversine formula
            location = nearest_place["geometry"]["location"]
            place_latitude = location["lat"]
            place_longitude = location["lng"]
            distance = calculate_distance(latitude, longitude, place_latitude, place_longitude)

            # Construct result dictionary
            result = {
                "name": nearest_place["name"],
                "vicinity": nearest_place["vicinity"],
                "location": location,
                "distance_km": distance
            }
            return result

    except requests.RequestException as e:
        print(f"Error retrieving nearest {place_type}: {e}")

    return None


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance (in kilometers) between two sets of coordinates using the Haversine formula.

    Args:
        lat1 (float): Latitude of point 1 (in degrees).
        lon1 (float): Longitude of point 1 (in degrees).
        lat2 (float): Latitude of point 2 (in degrees).
        lon2 (float): Longitude of point 2 (in degrees).

    Returns:
        float: Distance between the two points in kilometers.
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Radius of the Earth in kilometers
    radius = 6371.0

    # Calculate differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Calculate Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Calculate distance
    distance = radius * c
    return distance


def get_nearest_hospital(latitude, longitude, api_key):
    """
    Get the nearest hospital using Google Places API.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        api_key (str): Your Google Places API key.

    Returns:
        dict: Information about the nearest hospital, including name, vicinity, location, and distance.
    """
    return get_nearest_place(latitude, longitude, "hospital", api_key)


def get_nearest_fire_station(latitude, longitude, api_key):
    """
    Get the nearest fire station using Google Places API.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        api_key (str): Your Google Places API key.

    Returns:
        dict: Information about the nearest fire station, including name, vicinity, location, and distance.
    """
    return get_nearest_place(latitude, longitude, "fire_station", api_key)


def get_nearest_police_station(latitude, longitude, api_key):
    """
    Get the nearest police station using Google Places API.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        api_key (str): Your Google Places API key.

    Returns:
        dict: Information about the nearest police station, including name, vicinity, location, and distance.
    """
    return get_nearest_place(latitude, longitude, "police", api_key)

