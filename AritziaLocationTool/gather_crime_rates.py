import pandas as pd
from geopy.geocoders import Nominatim


def get_neighborhood(latitude, longitude):
    geolocator = Nominatim(user_agent="adenah9")
    location = geolocator.reverse([latitude, longitude], exactly_one=True)
    address = location.raw['address']
    neighborhood = address.get('neighbourhood', '')
    return neighborhood


def gather_safety_security_data(latitude, longitude):
    neighborhood = get_neighborhood(latitude, longitude)

    if not neighborhood:
        return {"message": "Unable to identify neighborhood for the provided coordinates."}

    crime_data = pd.read_csv('cleaned_toronto_crime_data.csv')
    crime_data_neighborhood = crime_data[crime_data['AREA_NAME'].str.contains(neighborhood)]

    if crime_data_neighborhood.empty:
        return {"message": f"No crime data available for the neighborhood: {neighborhood}"}

    crime_columns_2023 = [col for col in crime_data.columns if '2023' in col and 'RATE' not in col and 'POPULATION' not in col]
    crimes_2023 = crime_data_neighborhood[crime_columns_2023].sum(axis=1).values
    total_crimes_2023 = sum(crimes_2023)
    population_2023 = crime_data_neighborhood['POPULATION_2023'].values[0]
    crime_rate_2023 = (total_crimes_2023 / population_2023) * 100000

    return {
        "Neighborhood": neighborhood,
        "Total Crimes in 2023": total_crimes_2023,
        "Population in 2023": population_2023,
        "Crime Rate in 2023 per 100,000 people": crime_rate_2023
    }