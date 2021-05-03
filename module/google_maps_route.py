import polyline
from dotenv import load_dotenv
import googlemaps
import gmaps
import os

load_dotenv()
APIKEY = os.environ.get("APIKEY")
google_maps = googlemaps.Client(key=APIKEY)
gmaps.configure(api_key=APIKEY)


def plot_route(start, end, fig, color, stroke_weight_line, route_mode='walking'):
    directions_result = google_maps.directions(start, end, mode=route_mode)
    polyline_directions = polyline.decode(directions_result[0]['overview_polyline']['points'])

    polyline_result = [(a, b) for a, b in zip(polyline_directions, polyline_directions[1:])]
    for i in range(len(polyline_result)):
        line_drawing = gmaps.Line(start=polyline_result[i][0], end=polyline_result[i][1],
                                  stroke_weight=stroke_weight_line, stroke_color=color, stroke_opacity=1.0)
        drawing = gmaps.drawing_layer(features=[line_drawing], show_controls=False)
        fig.add_layer(drawing)