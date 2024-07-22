import speedtest
import requests


def get_internet_providers(latitude, longitude):
    """
    Get the top 3 internet service providers based on the closest servers to the given location.
    :param latitude:
    :param longitude:
    :return:
    """
    st = speedtest.Speedtest()
    servers = st.get_servers()

    for server in servers.values():
        for s in server:
            s['distance'] = ((float(s['lat']) - latitude)**2 + (float(s['lon']) - longitude)**2)**0.5

    sorted_servers = sorted([s for server in servers.values() for s in server], key=lambda s: s['distance'])

    top_isps = []
    for server in sorted_servers:
        if server['sponsor'] not in top_isps:
            top_isps.append(server['sponsor'])
        if len(top_isps) == 3:
            break

    return top_isps


def calculate_urbanization_level(latitude, longitude, api_key):
    """
    Calculate the urbanization level of a given location based on the administrative area level 2.
    :param latitude:
    :param longitude:
    :param api_key:
    :return:
    """
    api_url = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        "latlng": f"{latitude},{longitude}",
        "key": api_key
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()

        data = response.json()

        urbanization_level = 0.5

        if "results" in data and data["results"]:
            for result in data["results"]:
                for component in result["address_components"]:
                    if "administrative_area_level_2" in component["types"]:
                        urbanization_level = 0.8
                        break

        return urbanization_level

    except requests.RequestException as e:
        print(f"Error retrieving urbanization data: {e}")
        return 0.5


def assess_technology_infrastructure_without_population_density(latitude, longitude, api_key):
    """
    Assess the technology infrastructure of a given location based on the availability of internet service providers
    :param latitude:
    :param longitude:
    :param api_key:
    :return:
    """
    internet_providers = get_internet_providers(latitude, longitude)
    urbanization_level = calculate_urbanization_level(latitude, longitude, api_key)

    if internet_providers:
        infrastructure_score = 0.6 + (0.4 * urbanization_level)
    else:
        infrastructure_score = 0.2 + (0.3 * urbanization_level)

    return infrastructure_score, internet_providers, urbanization_level


