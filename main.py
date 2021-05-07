import argparse
from module import api_configuration
import warnings
warnings.filterwarnings("ignore")

def parser():
    parser = argparse.ArgumentParser(description='Specify inputs')
    parser.add_argument("-l",
                        "--location",
                        help="Please enter an address in the same way you enter it in Google Maps",
                        type=str,
                        default='Matadero Madrid'
                        )
    parser.add_argument("-m",
                        "--mode",
                        help="How are you going to get there? walking, driving, transit, bycicling?",
                        type=str,
                        default='walking')

    return parser.parse_args()

args= parser()

def main(location, mode):

    print('\n--- This is No More Gluten APP, the new hope for celiacs, gluten intolerants and posers! ---\n')
    print('So at this moment you are here:  \n' + location)
    print('\nAnd you say that your way of transport is: \n' +mode)
    print('\n---Getting data---\n')
    lat, lng, lat_current, lng_current = api_configuration.lat_lng_location(location)
    data = api_configuration.restaurants(lat, lng)
    dict_results, location_near, location_cheap, df = api_configuration.election(data)
    api_configuration.map_figure(dict_results, location_near, location_cheap, lat_current, lng_current, mode)
    print("---Please, go to the folder called Maps and find attached your html file with your route(s)---")
    print('\n--- PROCESS COMPLETED SUCCESSFULLY---\n')


if __name__ == '__main__':
        location = args.location
        mode = args.mode
        main(location, mode)