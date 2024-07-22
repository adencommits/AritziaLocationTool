from yelpapi import YelpAPI
import googlemaps


def get_driving_duration(origin, destination, gmaps):
    """
    Get driving duration from origin to destination using Google Maps Directions API
    :param origin:
    :param destination:
    :param gmaps:
    :return:
    """
    # Calculate driving duration using Google Maps Directions API
    directions = gmaps.directions(origin, destination, mode='driving')
    if directions:
        driving_time = directions[0]['legs'][0]['duration']['text']
        return driving_time
    else:
        return 'N/A'


def find_top_nearby_hotels_and_restaurants(latitude, longitude):
    # Initialize Yelp API client with your Yelp API Key
    yelp_api = YelpAPI('mkrjq_gEz32QjUVVzV2YJHve499a7TYmJoNaxoiWkNTjtD2ncBIS2A62s5t28GOxQW6WVH3M-ITFtm22XqEQCbvTL6Kd9h4wRhrxhzuoE_SmC2dOmXDSk3pAC6c_ZnYx')

    # Initialize Google Maps API client with your Google Maps API Key
    gmaps = googlemaps.Client(key='AIzaSyAEVMMBIjhk05WmXezmIlrBlg7IuhT3vzg')

    # Search for nearby hotels
    hotel_results = yelp_api.search_query(term='hotels',
                                           latitude=latitude,
                                           longitude=longitude,
                                           limit=3,  # Retrieve top 3 hotels
                                           sort_by='rating')  # Sort by highest rating

    # Search for nearby restaurants
    restaurant_results = yelp_api.search_query(term='restaurants',
                                               latitude=latitude,
                                               longitude=longitude,
                                               limit=5,  # Retrieve top 5 restaurants
                                               sort_by='rating')  # Sort by highest rating

    # Initialize lists to store hotel and restaurant data
    hotels = []
    restaurants = []

    # Process hotel results
    for hotel in hotel_results['businesses']:
        name = hotel['name']
        rating = hotel['rating']
        distance = f"{hotel['distance']:.2f} meters" if 'distance' in hotel else 'N/A'

        # Get driving duration from current location to the hotel
        driving_time = get_driving_duration((latitude, longitude), (hotel['coordinates']['latitude'], hotel['coordinates']['longitude']), gmaps)

        # Append hotel data to list
        hotels.append({
            "Name": name,
            "Rating": rating,
            "Distance": distance,
            "Driving Time": driving_time
        })

    # Process restaurant results
    for restaurant in restaurant_results['businesses']:
        name = restaurant['name']
        rating = restaurant['rating']
        distance = f"{restaurant['distance']:.2f} meters" if 'distance' in restaurant else 'N/A'

        # Get driving duration from current location to the restaurant
        driving_time = get_driving_duration((latitude, longitude), (restaurant['coordinates']['latitude'], restaurant['coordinates']['longitude']), gmaps)

        # Append restaurant data to list
        restaurants.append({
            "Name": name,
            "Rating": rating,
            "Distance": distance,
            "Driving Time": driving_time
        })

    # Return hotel and restaurant data
    return hotels, restaurants