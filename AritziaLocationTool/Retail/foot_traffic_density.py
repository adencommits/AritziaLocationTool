import time
import googlemaps

# Initialize Google Maps client with your API key
gmaps = googlemaps.Client(key='AIzaSyAEVMMBIjhk05WmXezmIlrBlg7IuhT3vzg')


def get_establishment_count(latitude, longitude, radius=1500):
    # Define weights for different types of establishments
    weights = {
        'shopping_mall': 3,
        'stadium': 3,
        'airport': 3,
        'train_station': 2,
        'subway_station': 2,
        'bus_station': 2,
        'store': 3,  # Increase weight for 'store'
        'restaurant': 3,  # Increase weight for 'restaurant'
        'cafe': 3  # Increase weight for 'cafe'
    }

    # Initialize count with 0
    count = 0

    # Use Google Places API to find establishments of each type around the given coordinates
    for type, weight in weights.items():
        places_result = gmaps.places_nearby(location=(latitude, longitude), radius=radius, type=type)

        # Add the weighted number of establishments in the first page of results to the count
        count += weight * len(places_result['results'])

        # Use pagination to retrieve all results
        while 'next_page_token' in places_result:
            # Wait for a short delay before making the next request
            time.sleep(2)

            # Retry the request until it succeeds
            while True:
                try:
                    # Make the next request
                    places_result = gmaps.places_nearby(page_token=places_result['next_page_token'])

                    # If the request was successful, break the loop
                    break
                except:
                    # If the request failed, wait for a short delay before retrying
                    time.sleep(2)

            # Add the weighted number of establishments in this page of results to the count
            count += weight * len(places_result['results'])

    return count

def get_foot_traffic_score(latitude, longitude, max_establishments=600):  # Decrease max_establishments
    # Get the weighted number of establishments around the given coordinates
    establishment_count = get_establishment_count(latitude, longitude)

    # Normalize the establishment count to get a foot traffic score between 0 and 1
    foot_traffic_score = min(establishment_count / max_establishments, 1)

    return foot_traffic_score

