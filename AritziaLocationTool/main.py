import community_ammenities
import gather_crime_rates
import technology_infrastructure
import nearby_public_bus_stops
import airport_accessibility
import community_ammenities
import nearest_emergency_locations
from geopy.geocoders import Nominatim


api_key = 'AIzaSyAEVMMBIjhk05WmXezmIlrBlg7IuhT3vzg'


def address_to_coordinates(address):
    """
    Convert an address to latitude and longitude coordinates
    :param address:
    :return:
    """
    geolocator = Nominatim(user_agent="adencommits")
    location = geolocator.geocode(address)
    return location.latitude, location.longitude


def main():
    """
    Main function to run the analysis
    :return:
    """

    with open('coordinates.txt', 'r') as f:
        coordinates = f.read().split(',')
        latitude = float(coordinates[0])
        longitude = float(coordinates[1])

    nearest_hospital = nearest_emergency_locations.get_nearest_hospital(latitude, longitude, api_key)
    nearest_fire_station = nearest_emergency_locations.get_nearest_fire_station(latitude, longitude, api_key)
    nearest_police_station = nearest_emergency_locations.get_nearest_police_station(latitude, longitude, api_key)

    infrastructure_score, internet_providers, urbanization_level = technology_infrastructure.assess_technology_infrastructure_without_population_density(
        latitude, longitude, api_key)

    data = {}

    data['Coordinates'] = {
        'latitude': latitude,
        'longitude': longitude
    }

    data['Safety & Security Data'] = gather_crime_rates.gather_safety_security_data(latitude, longitude)

    data['Technology Infrastructure'] = {
        'score':
            technology_infrastructure.assess_technology_infrastructure_without_population_density(latitude, longitude,
                                                                                                  api_key)[0],
        'internet_providers':
            technology_infrastructure.assess_technology_infrastructure_without_population_density(latitude, longitude,
                                                                                                  api_key)[1],
        'urbanization_level':
            technology_infrastructure.assess_technology_infrastructure_without_population_density(latitude, longitude,
                                                                                                  api_key)[2]
    }

    # Get nearby bus stops
    bus_stops = nearby_public_bus_stops.analyze_location_factors(latitude, longitude, api_key)
    data['Public Bus Stops'] = bus_stops

    data['Airport Accessibility'] = airport_accessibility.assess_accessibility(latitude, longitude)

    data['Community Amenities'] = {}
    data['Community Amenities']['Hotels'], data['Community Amenities'][
        'Restaurants'] = community_ammenities.find_top_nearby_hotels_and_restaurants(latitude, longitude)

    weather_data = get_historical_weather_data(latitude, longitude, 'B7BXX88URLD3K2SG6EPU28N4G')
    if weather_data:
        data['Geological Risk'] = {
            season.capitalize(): f"{precipitation:.2f} mm per day" for season, precipitation in
            calculate_seasonal_precipitation(weather_data).items()
        }

    data['Nearest Emergency Locations'] = {
        'Nearest Hospital': nearest_hospital,
        'Nearest Fire Station': nearest_fire_station,
        'Nearest Police Station': nearest_police_station
    }

    return data


if __name__ == "__main__":
    main()
