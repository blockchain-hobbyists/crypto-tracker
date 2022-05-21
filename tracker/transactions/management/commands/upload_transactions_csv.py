from decimal import Decimal
from django.core.management.base import BaseCommand
import pytz
from transactions.models import OrderType, Transaction, Exchange
from assets.models import Pair
from django.conf import settings
from django.contrib.auth.models import User
import csv
import os
from datetime import datetime


class Command(BaseCommand):
    """
        Format : DATE_TIME | PAIR | ORDER_TYPE | EXCHANGE | PRICE | AMOUNT | FEE | USERNAME
    """

    help = 'Uploads user transactions from csv file'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Full path to csv file',
                            default=os.path.join(settings.BASE_DIR, 'transactions.csv'))

    def handle(self, *args, **options):
        with open(options['path'], newline='', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter='|')
            for row in spamreader:
                base, quote = row[1].split('-')[0], row[1].split('-')[1]
                pair = Pair.objects.get(base__name=base, quote__name=quote)
                order_type = OrderType.objects.get(name=row[2].strip())
                exchange = Exchange.objects.get(name=row[3].strip())
                price = Decimal(row[4])
                amount = Decimal(row[5])
                fee = Decimal(row[6])
                user = User.objects.get(username=row[7])
                Transaction.objects.create(
                    pair=pair, exchange=exchange, order_type=order_type,
                    price=price, avg_filling_price=price,
                    amount=amount, fee=fee, user=user, ts=datetime.strptime(row[0], '%m/%d/%Y %H:%M:%S').replace(tzinfo=pytz.UTC))
