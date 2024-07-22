import requests
from geopy.geocoders import Nominatim
import time
from geopy.exc import GeocoderTimedOut


def get_city_state(latitude, longitude):
    geolocator = Nominatim(user_agent="adenah04")
    location = None
    while location is None:
        try:
            location = geolocator.reverse([latitude, longitude], exactly_one=True)
        except GeocoderTimedOut:
            time.sleep(1)
    address = location.raw['address']
    city = address.get('city', '')
    state = address.get('state', '')
    print(f"City: {city}, State: {state}")  # Debugging line
    return city, state

def get_crime_rate(latitude, longitude):
    city, state = get_city_state(latitude, longitude)
    if city and state:
        # Replace 'your_api_key' with your actual API key
        url = f"https://api.usa.gov/crime/fbi/sapi/api/summarized/agencies/{state}/{city}/violent_crime/2019/2019?api_key=S29zWpJ4vwZ3WFek2zIeN3wfTQGZj7ptOd5TlOiL"
        response = requests.get(url)
        data = response.json()
        print(f"Data: {data}")  # Debugging line
        if 'results' in data:
            return data['results']
    return None

latitude = 39.29993461377201
longitude = -76.60415315303186
print(get_crime_rate(latitude, longitude))