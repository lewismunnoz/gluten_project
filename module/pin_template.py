
def template(dict_results):
    info_box_template = """
    <dl>
    <dt>Establecimiento:</dt><dd>{name}</dd>
    <dt>Tipo de comida:</dt><dd>{types}</dd>
    <dt>Precio:</dt><dd>{price_level}/4.0</dd>
    <dt>Puntuaciones de Google Maps:</dt><dd>{rating} en {user_ratings_total} evaluaciones</dd>

    <dt>Dirección:</dt><dd>{vicinity}</dd>
    </dl>
    """
    restaurant_info = [info_box_template.format(**food) for food in dict_results]
    return restaurant_info
