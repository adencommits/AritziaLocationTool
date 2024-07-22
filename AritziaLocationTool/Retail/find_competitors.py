import googlemaps


def find_competitors(latitude, longitude, radius=1000):
    # Initialize Google Maps client with your API key
    gmaps = googlemaps.Client(key='AIzaSyAEVMMBIjhk05WmXezmIlrBlg7IuhT3vzg')

    # Define Aritzia's main competitors
    competitors = ['Zara', 'H&M', 'Forever 21', 'Uniqlo', 'Gap', 'Banana Republic',
                   'Frank And Oak', 'Garage', 'American Eagle', 'Urban Outfitters',
                   'Abercrombie & Fitch', 'Hollister', 'Topshop', 'Lululemon', 'Nike',
                   'Adidas', 'Free People', 'Club Monaco', 'REVOLVE', 'ASOS', 'Nordstrom',
                   'Saks Fifth Avenue', 'Bloomingdale\'s', 'Macy\'s', 'Neiman Marcus']

    # Initialize a dictionary to store competitor locations
    competitor_locations = {competitor: [] for competitor in competitors}

    # Search for each competitor
    for competitor in competitors:
        # Use the Google Places API to find nearby businesses with the competitor's name
        places_result = gmaps.places_nearby(location=(latitude, longitude), radius=radius, keyword=competitor)

        # Add the locations of the competitor's stores to the dictionary
        for result in places_result['results']:
            # Check if the business is a clothing store
            if 'clothing_store' in result['types']:
                # Calculate walking distance from the selected coordinates to the store
                store_location = (result['geometry']['location']['lat'], result['geometry']['location']['lng'])
                distance_result = gmaps.distance_matrix(origins=(latitude, longitude), destinations=store_location, mode='walking')
                distance = distance_result['rows'][0]['elements'][0]['distance']['text']

                competitor_locations[competitor].append({
                    'Name': result['name'],
                    'Address': result['vicinity'],
                    'Distance': distance
                })

    return competitor_locations
