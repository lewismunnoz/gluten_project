import pandas as pd
import requests
import googlemaps
import gmaps
import gmaps.datasets
from module import pin_template
from module import google_maps_route
from ipywidgets.embed import embed_minimal_html
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(".env"), '.env')
load_dotenv(dotenv_path)
APIKEY = os.environ.get("APIKEY")


def lat_lng_current_location(current_location):
    gmaps_google = googlemaps.Client(key=APIKEY)
    geocode = gmaps_google.geocode(current_location)

    lat = str(geocode[0]['geometry']['location']['lat'])
    lng = str(geocode[0]['geometry']['location']['lng'])
    lat_current = geocode[0]['geometry']['location']['lat']
    lng_current = geocode[0]['geometry']['location']['lng']
    return lat, lng, lat_current, lng_current


def restaurants(lat, lng):

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+lat+","+lng +\
          "&keyword=gluten_free&type=restaurant&language=es&rankby=distance&pagetoken&key="+APIKEY
    url_result = requests.get(url)
    url_result_convert = url_result.json()
    data = pd.json_normalize(url_result_convert['results'])
    if data.empty is True:
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + lat + "," + \
              lng + "&radius=10000&type=atm&language=es&key=" + APIKEY
        url_result = requests.get(url)
        url_result_convert = url_result.json()
        data = pd.json_normalize(url_result_convert['results'])
    restaurant_db_row = data[['name', 'place_id', 'rating', 'types', 'vicinity', 'price_level', 'user_ratings_total',
                              'geometry.location.lat', 'geometry.location.lng', 'opening_hours.open_now', 'icon']]
    restaurant_db_row.dropna(subset=["price_level"], inplace=True)
    restaurant_db = restaurant_db_row

    restaurant_db.to_csv('./data/processed/restaurant_db.csv', index=False)
    return restaurant_db


def election(restaurant_db):
    location_near = (restaurant_db['geometry.location.lat'].iloc[0], restaurant_db['geometry.location.lng'].iloc[0])
    cheap_restaurant = restaurant_db.sort_values("price_level")
    location_cheap = (cheap_restaurant['geometry.location.lat'].iloc[0],
                      cheap_restaurant['geometry.location.lng'].iloc[0])
    dict_results = restaurant_db.to_dict('records')

    return dict_results, location_near, location_cheap, cheap_restaurant


def map_figure(dict_results, location_near, location_cheap, lat_current, lng_current, route_mode):
    locations = [(rows_result['geometry.location.lat'],
                  rows_result['geometry.location.lng']) for rows_result in dict_results]
    restaurant_info = pin_template.template(dict_results)
    fig = gmaps.figure()
    now_location = [(lat_current, lng_current)]
    marker_layer = gmaps.marker_layer(now_location)
    fig.add_layer(marker_layer)

    symbol_layer = gmaps.symbol_layer(locations, info_box_content=restaurant_info, scale=6, stroke_color="teal")
    index_free = int("".join([str(integer) for integer in
                              [i for i in range(len(locations)) if locations[i] == location_near]]))
    symbol_layer.markers[index_free].stroke_color = 'yellow'
    google_maps_route.plot_route((lat_current, lng_current), location_near, fig, 'yellow', 7.0, route_mode)

    print("\n  Done!")

    if location_near != location_cheap:
        index_near = int("".join([str(integer) for integer in
                                  [i for i in range(len(locations)) if locations[i] == location_cheap]]))
        symbol_layer.markers[index_near].stroke_color = 'green'
        google_maps_route.plot_route((lat_current, lng_current), location_cheap, fig, 'green', 3.5, route_mode)
        print("\n  The cheapest gluten_free restaurant is the one marked in the yellow route"
              " and the nearest one on the green route  \n")
    else:
        print("\n  The nearest one is also the cheapest one :)!  \n")

    fig.add_layer(symbol_layer)

    embed_minimal_html('.export.html', views=[fig])
