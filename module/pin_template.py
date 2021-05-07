
def template(dict_results):
    info_box_template = """
    <dl>
    </dl>Name: {name}</dl>
    <dl>Type of food you may find:</dt><dd>{types}</dl>
    <dl>Price Level (1-4): {price_level}/4.0</dl>
    <dl>Google Rating: {rating} en {user_ratings_total} evaluaciones</dl>
    <dl>Address: <a href="https://www.google.es/maps/search/{vicinity}">{vicinity}</a></dl>
    </dl>
    """
    restaurant_info = [info_box_template.format(**food) for food in dict_results]
    return restaurant_info
