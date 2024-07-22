import requests

def find_local_events(latitude, longitude, distance=1000):
    # Facebook Graph API endpoint
    url = "https://graph.facebook.com/v13.0/search"

    # Define the parameters for the API request
    params = {
        "type": "event",
        "center": f"{latitude},{longitude}",
        "distance": distance,
        "fields": "name,start_time,end_time,place",
        "access_token": "YOUR_FACEBOOK_ACCESS_TOKEN"
    }

    # Send a GET request to the Facebook Graph API
    response = requests.get(url, params=params)

    # If the request was successful, print the names and addresses of the local events
    if response.status_code == 200:
        events = response.json()["data"]
        for event in events:
            print(f"Event Name: {event['name']}")
            print(f"Event Start: {event['start_time']}")
            print(f"Event End: {event['end_time']}")
            if 'place' in event:
                print(f"Venue Name: {event['place']['name']}")
                if 'location' in event['place']:
                    print(f"Venue Address: {event['place']['location']['street']}")
            print("\n")
    else:
        print(f"Error: {response.status_code}")

# Replace with the actual latitude and longitude
latitude = 43.67029848772484
longitude = -79.43515535336972

find_local_events(latitude, longitude)