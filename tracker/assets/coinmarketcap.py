

from datetime import datetime
import requests
import pprint

from .models import Pair, PairPrice
import os

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

QUOTE = 'EUR'

parameters = {
    'slug': 'bitcoin',
    'convert': QUOTE
}

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': os.environ.get('X-CMC_PRO_API_KEY')
}


def get_pair_price(pair: Pair) -> PairPrice:
    """
    """
    pair_data = requests.get(url, params=parameters, headers=headers).json()
    price = pair_data['data']['1']['quote'][QUOTE]['price']
    return PairPrice(pair=pair, price=price, ts=datetime.now())

#session = Request()
# session.headers.update(headers)


json = requests.get(url, params=parameters, headers=headers).json()
print("\n\n\n Toda la informacion sobre la moneda\n\n\n")
pprint.pprint(json)
# Hay que tener en cuenta que hay un time stamp cada 60 segundos y el precio no se actualizara hasta entonces
print("\n\n\n Solo el precio\n\n\n")
pprint.pprint(json['data']['1']['quote'][QUOTE]['price'])
# Asi crearemos un archivo con el precio de cada moneda
# coins = json['data']
