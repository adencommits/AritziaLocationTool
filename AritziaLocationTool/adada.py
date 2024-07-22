print(f"Coordinates read from file: {latitude}, {longitude}")

print("\n--- Safety & Security Data ---")
gather_crime_rates.gather_safety_security_data(latitude, longitude)

print("\n--- Technology Infrastructure ---")
infrastructure_score, internet_providers, urbanization_level = technology_infrastructure.assess_technology_infrastructure_without_population_density(
    latitude, longitude, api_key)
print(f"Technology Infrastructure Score: {infrastructure_score}")
print(f"Internet Service Providers: {internet_providers}")
print(f"Urbanization Level: {urbanization_level}")

print("\n--- Public Bus Stops ---")
nearby_public_bus_stops.analyze_location_factors(latitude, longitude, api_key)

print("\n--- Airport Accessibility ---")
airport_accessibility.assess_accessibility(latitude, longitude)

print("\n--- Community Amenities ---")
community_ammenities.find_top_nearby_hotels_and_restaurants(latitude, longitude)

print("\n--- Geological Risk ---")

weather_data = get_historical_weather_data(latitude, longitude,
                                           'B7BXX88URLD3K2SG6EPU28N4G')  # replace with your Visual Crossing API key
if weather_data:
    average_precipitation = calculate_seasonal_precipitation(weather_data)
    for season, precipitation in average_precipitation.items():
        print(f"The average precipitation in {season.capitalize()} 2023 is {precipitation:.2f} mm per day.")

print("\n--- Nearest Emergency Locations ---")
nearest_hospital = nearest_emergency_locations.get_nearest_hospital(latitude, longitude, api_key)
nearest_fire_station = nearest_emergency_locations.get_nearest_fire_station(latitude, longitude, api_key)
nearest_police_station = nearest_emergency_locations.get_nearest_police_station(latitude, longitude, api_key)

if nearest_hospital:
    print("Nearest Hospital:")
    print(f"Name: {nearest_hospital['name']}")
    print(f"Address: {nearest_hospital['vicinity']}")
    print(f"Distance: {nearest_hospital['distance_km']:.2f} km")

if nearest_fire_station:
    print("\nNearest Fire Station:")
    print(f"Name: {nearest_fire_station['name']}")
    print(f"Address: {nearest_fire_station['vicinity']}")
    print(f"Distance: {nearest_fire_station['distance_km']:.2f} km")

if nearest_police_station:
    print("\nNearest Police Station:")
    print(f"Name: {nearest_police_station['name']}")
    print(f"Address: {nearest_police_station['vicinity']}")
    print(f"Distance: {nearest_police_station['distance_km']:.2f} km")