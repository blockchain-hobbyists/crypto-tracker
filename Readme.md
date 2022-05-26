# CRYPTO-TRACKER

[![Python Badge](https://img.shields.io/badge/python-3.10-blue.svg)]()
[![Main](https://github.com/blockchain-hobbyists/crypto-tracker/actions/workflows/main.yml/badge.svg)](https://github.com/blockchain-hobbyists/crypto-tracker/actions/workflows/main.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=blockchain-hobbyists_crypto-tracker&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=blockchain-hobbyists_crypto-tracker)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=blockchain-hobbyists_crypto-tracker&metric=coverage)](https://sonarcloud.io/summary/new_code?id=blockchain-hobbyists_crypto-tracker)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=blockchain-hobbyists_crypto-tracker&metric=bugs)](https://sonarcloud.io/summary/new_code?id=blockchain-hobbyists_crypto-tracker)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=blockchain-hobbyists_crypto-tracker&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=blockchain-hobbyists_crypto-tracker)

Crypto-Tracker pretends to be a useful application for traders providing a simple interface to track crypto transactions.

## How it works

1. Configure your assets and exchanges
2. Install the app
3. Configure your assets and exchanges
4. Create or import transactions
5. Keep your asset balances updated
6. Get insights from your assets or market movements

## Configure settings and environment variables

### Settings example

```python
ASSETS = [
    'USD',
    'BTC',
]
EXCHANGES = [
    ('Gemini', ['Limit Buy','Limit Sell']),
]
```

### .env file example

```bash
COINMARKETCAP_API_KEY=<YOUR_KEY>
POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DJANGO_SETTINGS_MODULE=settings.postgres
PORT=8000
```

## Install

### Python environment

- python 3.10
- `pipenv install` or `pip install -r requirements.txt`

```bash
python tracker/manage.py migrate
python tracker/manage.py createsuperuser
python tracker/manage.py collectstatic
python tracker/manage.py runserver
```

## Docker compose

```bash
docker-compose up
```

## Configure tracker/settings/base.py

```python
ASSETS = [
    'USD',
    'BTC',
]
EXCHANGES = [
    ('Gemini', ['Limit Buy','Limit Sell']),
]
```

## Update DB

```bash
python tracker/manage.py upsert_all_meta
```

## Check Admin UI at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Import transactions from csv

Save a file like this one as transactions.csv in root folder.

**Do not include headers**

```
DATE_TIME | PAIR | ORDER_TYPE | EXCHANGE | PRICE | AMOUNT | FEE | USERNAME
---------------------------------------------------------------------------
```

```csv
05/02/2022 11:22:38|BTC-USD|Limit Buy|Gemini|200.32|0.21465654|0|Gretzky
05/03/2022 11:22:38|USD-BTC|Limit Sell|Gemini|910.91|0.1635178|1.05|Gretzky
```

Run import command `python tracker/manage.py upload_transactions_csv`
or `python tracker/manage.py upload_transactions_csv --path full-path-to-csv`

## Pair prices sync

Coinmarketcap API is used to get pairs prices. By default, the quote currency is EUR.

Change Coinmarketcap settings to modify its behaviour. Every QUOTE - BASE combination configured will be requested to the API.

```python
COINMARKETCAP = {
    'API_KEY': os.environ.get('COINMARKETCAP_API_KEY', ''),
    'QUOTE': 'EUR',
    'BASES': ['BTC', 'ETH', 'SOL', 'ALGO']
}
```

Run the command `python tracker/manage.py update_pair_prices` to update prices.
Run the command `python tracker/manage.py update_pair_prices --infinite-run` to keep updating prices every minute.
