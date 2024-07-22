from Retail.find_competitors import find_competitors
from Retail.foot_traffic_density import get_foot_traffic_score
from Retail.gather_crime_rates import gather_safety_security_data
from Retail.nearby_public_bus_stops import analyze_location_factors
import json
import os
import numpy as np

# Define the coordinates and API key
# Read the coordinates from the file

# Get the absolute path to the coordinates.txt file
coordinates_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'coordinates.txt')

with open(coordinates_file_path, 'r') as file:
    coordinates = file.read().split(',')

# Convert the coordinates to float
latitude = float(coordinates[0])
longitude = float(coordinates[1])

# Rest of your code...
api_key = 'AIzaSyAEVMMBIjhk05WmXezmIlrBlg7IuhT3vzg'


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyEncoder, self).default(obj)


def main_retail():
    # Call the functions from the other scripts and save the results
    competitors = find_competitors(latitude, longitude)
    foot_traffic_score = get_foot_traffic_score(latitude, longitude)
    safety_security_data = gather_safety_security_data(latitude, longitude)
    location_factors = analyze_location_factors(latitude, longitude, api_key)

    # Create a dictionary to store all the results
    data = {'Coordinates': {
        'latitude': latitude,
        'longitude': longitude
    }, 'Competitors': competitors, 'Foot Traffic Density': foot_traffic_score,
        'Safety & Security Data': safety_security_data, 'Public Bus Stops': location_factors}

    data_string = json.dumps(data, cls=NumpyEncoder)

    return data_string


if __name__ == '__main__':
    result = main_retail()
    print(result)


