import googlemaps
import datetime
import pytz


def assess_accessibility(latitude, longitude):
    gmaps = googlemaps.Client(key='AIzaSyAEVMMBIjhk05WmXezmIlrBlg7IuhT3vzg')
    warehouse_location = (latitude, longitude)
    places_result = gmaps.places_nearby(location=warehouse_location, radius=50000, type='airport')

    result = {}

    if 'results' in places_result and places_result['results']:
        nearest_airport = places_result['results'][0]
        nearest_airport_location = nearest_airport['geometry']['location']

        # Add the name of the airport to the result
        result['Nearest Airport'] = nearest_airport['name']

        # Define the desired times of departure in EST
        est = pytz.timezone('US/Eastern')
        now = datetime.datetime.now(est)
        departure_times = [now + datetime.timedelta(hours=h) for h in [1, 4, 7, 9]]  # 1, 4, 7, and 9 hours from now

        directions = gmaps.directions(warehouse_location, nearest_airport_location, mode='driving', departure_time=departure_times[0])

        if directions:
            drive_distance = directions[0]['legs'][0]['distance']['text']
            result['Drive Distance'] = drive_distance

            result['ETAs'] = []
            for departure_time in departure_times:
                directions = gmaps.directions(warehouse_location, nearest_airport_location, mode='driving', departure_time=departure_time)

                if directions:
                    drive_eta = directions[0]['legs'][0]['duration_in_traffic']['text']
                    result['ETAs'].append({f"Drive ETA at {departure_time.hour}:00 EST": drive_eta})
                else:
                    result['ETAs'].append("No directions found.")
        else:
            result['message'] = "No directions found."
    else:
        result['message'] = "No airports found within the specified radius."

    return result