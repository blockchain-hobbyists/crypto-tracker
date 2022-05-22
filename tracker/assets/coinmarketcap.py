from .models import Pair, PairPrice
import requests
import pytz
from datetime import datetime
import os

COINMARKETCAP_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': os.environ.get('COINMARKETCAP_API_KEY')
}


def get_pair_price(pair: Pair) -> PairPrice:
    """
    Crate a PairPrice object for Pair with coinmarketcap API
    """

    parameters = {
        'symbol': pair.base.name, 'convert': pair.quote.name}
    pair_data = requests.get(
        COINMARKETCAP_URL,
        params=parameters,
        headers=headers
    ).json()
    price = pair_data['data'][pair.base.name]['quote'][pair.quote.name]['price']
    return PairPrice(pair=pair, price=price, ts=datetime.now(tz=pytz.UTC))
