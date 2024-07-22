import requests
import datetime


def get_seasonal_weather(api_key, latitude, longitude, year):
    # Visual Crossing Weather API endpoint for historical weather
    url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{},{}/{}-01-01/{}-12-31".format(
        latitude, longitude, year, year)

    params = {
        'key': api_key,
        'unitGroup': 'metric'
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None


def process_seasonal_data(weather_data):
    # Define the time period for each season (Northern Hemisphere)
    seasons = {
        'Winter': [(1, 1), (3, 20)],
        'Spring': [(3, 21), (6, 20)],
        'Summer': [(6, 21), (9, 22)],
        'Fall': [(9, 23), (12, 20)]
    }

    seasonal_data = {season: [] for season in seasons}

    for day in weather_data['days']:
        date = datetime.datetime.strptime(day['datetime'], '%Y-%m-%d')
        for season, (start, end) in seasons.items():
            start_date = datetime.datetime(date.year, *start)
            end_date = datetime.datetime(date.year, *end)
            if start_date <= date <= end_date:
                seasonal_data[season].append(day)
                break

    return seasonal_data


# Example usage
if __name__ == "__main__":
    # Replace with your actual API key
    API_KEY = 'B7BXX88URLD3K2SG6EPU28N4G'
    LATITUDE = 49.2827  # Example latitude (Vancouver, Canada)
    LONGITUDE = -123.1207  # Example longitude (Vancouver, Canada)
    YEAR = 2023

    weather_data = get_seasonal_weather(API_KEY, LATITUDE, LONGITUDE, YEAR)

    if weather_data:
        seasonal_patterns = process_seasonal_data(weather_data)

        # Print collected seasonal weather data for inspection
        for season, data in seasonal_patterns.items():
            print(f"Weather data for {season}:")
            for entry in data:
                print(entry)
