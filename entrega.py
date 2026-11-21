import urllib.parse
from geopy.distance import geodesic
from geopy.geocoders import Nominatim


def calcular_entrega(endereco_loja, endereco_cliente, valor_por_km=2.50, taxa_minima=5.00):
    geolocator = Nominatim(user_agent="sistema_lanchonete_app")

    loc_loja = geolocator.geocode(endereco_loja)
    loc_cliente = geolocator.geocode(endereco_cliente)

    if not loc_loja or not loc_cliente:
        return None, None, "Endereço não encontrado."

    coord_loja = (loc_loja.latitude, loc_loja.longitude)
    coord_cliente = (loc_cliente.latitude, loc_cliente.longitude)

    distancia_km = geodesic(coord_loja, coord_cliente).km * 1.3
    valor_frete = max(taxa_minima, round(distancia_km * valor_por_km, 2))

    destino_encoded = urllib.parse.quote(endereco_cliente)
    link_mapa = f"https://www.google.com/maps/dir/?api=1&destination={destino_encoded}"

    return round(distancia_km, 2), valor_frete, link_mapa
