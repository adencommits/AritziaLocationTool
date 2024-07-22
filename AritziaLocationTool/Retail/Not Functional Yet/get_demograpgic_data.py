import requests
import pandas as pd

def get_geographic_region(lat, lon, geocoding_api_key):
    geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={geocoding_api_key}"
    response = requests.get(geocoding_url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            address_components = data['results'][0]['address_components']
            city = None
            province = None
            for component in address_components:
                if 'locality' in component['types']:
                    city = component['long_name']
                if 'administrative_area_level_1' in component['types']:
                    province = component['long_name']
            return city, province
    return None, None

def load_population_density_data(file_path):
    df = pd.read_csv(file_path)
    return df

def get_population_density(df, province):
    # Filter the dataframe for the given province
    province_data = df[df['Province'] == province]
    if not province_data.empty:
        return province_data
    else:
        return None

def main(geocoding_api_key, latitude, longitude, population_density_file):
    city, province = get_geographic_region(latitude, longitude, geocoding_api_key)
    if city or province:
        print(f"City: {city}, Province: {province}")
        df = load_population_density_data(population_density_file)
        population_density = get_population_density(df, province)
        if population_density is not None:
            print(f"Population density data for {province}:")
            print(population_density)
        else:
            print(f"No population density data found for {province}.")
    else:
        print("Failed to determine geographic region from coordinates.")

if __name__ == "__main__":
    # Example usage
    GEOCODING_API_KEY = 'AIzaSyAEVMMBIjhk05WmXezmIlrBlg7IuhT3vzg'
    LATITUDE = 49.2827  # Example latitude (Vancouver, Canada)
    LONGITUDE = -123.1207  # Example longitude (Vancouver, Canada)
    POPULATION_DENSITY_FILE = 'path_to_population_density_file.csv'  # Path to your population density CSV file

    main(GEOCODING_API_KEY, LATITUDE, LONGITUDE, POPULATION_DENSITY_FILE)
