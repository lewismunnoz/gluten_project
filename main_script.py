import argparse

from module import api_configuration




def main(current_location, route_mode):
    print('\n--- Comenzamos! ---\n')
    print('Comamos gluten en:\n' + current_location.title())
    lat, lng, lat_current, lng_current = api_configuration.lat_lng_current_location(current_location)
    data = api_configuration.restaurants(lat, lng)
    dict_results, location_near, location_cheap = api_configuration.election(data)
    api_configuration.map_figure(dict_results, location_near, location_cheap, lat_current, lng_current, route_mode)
    print('\n--- FIN ---\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--current_location", help="Please enter an address", dest='current_location',
                        default='Estadio Santiago Bernabeu')
    parser.add_argument("-m", "--route_mode", help="how are you getting there?", dest='route_mode',
                        default='walking')
    args = parser.parse_args()
    current_location = args.current_location
    route_mode = args.route_mode
    main(current_location, route_mode)
