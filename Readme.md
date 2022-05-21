# CRYPTO-TRACKER

[![Python Badge](https://img.shields.io/badge/python-3.10-blue.svg)]()
![example workflow](https://github.com/blockchain-hobbyists/crypto-tracker/actions/workflows/main.yml/badge.svg)

Crypto-Tracker pretends to be a useful application for traders providing a simple interface to track crypto transactions.

## How it works

1. Install the app
2. Configure your assets and exchanges
3. Create or import transactions
4. Keep your asset balances updated
5. Get insights from your assets or market movements

## Install

- python 3.10
- `pipenv install` or `pip install -r requirements.txt`

```bash
python tracker/manage.py migrate
python tracker/manage.py createsuperuser
python tracker/manage.py collectstatic
python tracker/manage.py runserver
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

http://127.0.0.1:8000/admin/

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
