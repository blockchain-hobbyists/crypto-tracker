from decimal import Decimal
from datetime import datetime
import pytz
from django.test import TestCase
from django.core import management
from django.contrib.auth.models import User

from transactions.models import Exchange, OrderType, Pair, Transaction
from assets.models import Asset
from users.models import Balance


class TransactionTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        management.call_command('upsert_all_meta')

    def test_assets(self):
        """
            Example Transaction
        """
        btc = Asset.objects.get(name='BTC')
        eur = Asset.objects.get(name='EUR')
        pair = Pair.objects.get(base=btc, quote=eur)
        user = User.objects.get(username='myuser')
        exchange = Exchange.objects.first()
        order_type = OrderType.objects.first()

        # Add founds 100€, 0 BTC
        Balance.objects.update_or_create(
            user=user, asset=eur, defaults={'amount': 100})
        Balance.objects.update_or_create(
            user=user, asset=btc, defaults={'amount': 0})

        # Executed BTC-EUR limit buy order
        Transaction.objects.create(
            pair=pair, exchange=exchange, order_type=order_type,
            price=29800.00, avg_filling_price=29800.00,
            amount=0.0033557, fee=0.40, user=user, ts=datetime.now(tz=pytz.UTC))

        # Verify new balances amounts
        euros = Balance.objects.get(
            user=user, asset=eur).amount
        btcs = Balance.objects.get(user=user, asset=btc).amount
        self.assertAlmostEqual(btcs, Decimal(0.0033557), delta=1)
        self.assertAlmostEqual(euros, 0, delta=1)
