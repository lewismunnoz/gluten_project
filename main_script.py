import argparse
import pandas as pd
from module import api_configuration


def main(current_location, mode):
    print('\n--- Comenzamos! ---\n')
    print('Comamos gluten en:\n' + current_location)
    lat, lng, lat_current, lng_current = api_configuration.lat_lng_current_location(current_location)
    data = api_configuration.restaurants(lat, lng)
    dict_results, location_near, location_cheap, df = api_configuration.election(data)
    api_configuration.map_figure(dict_results, location_near, location_cheap, lat_current, lng_current, mode)
    print('\n--- FIN ---\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--current_location", help="Please enter an address", dest='current_location',
                        default='Jacinto Benavente Madrid')
    parser.add_argument("-m", "--route_mode", help="how are you getting there?", dest='mode',
                        default='walking')
    args = parser.parse_args()
    current_location = args.current_location
    mode = args.mode
    main(current_location, mode)
