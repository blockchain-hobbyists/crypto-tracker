from decimal import Decimal

from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.db import transaction
from django.contrib.auth.models import User

from assets.models import Pair
from users.models import Balance


class Exchange(models.Model):
    """
        Exchange
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return f'{self.name }'


class OrderType(models.Model):
    """
        Type of order
    """
    id = models.BigAutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self) -> str:
        return f'{self.name }'


class Transaction(models.Model):
    """
        Transaction made by user on exchange with an asser pair
    """
    id = models.BigAutoField(primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=DO_NOTHING)
    pair = models.ForeignKey(Pair, on_delete=DO_NOTHING)
    exchange = models.ForeignKey(Exchange, on_delete=DO_NOTHING)
    order_type = models.ForeignKey(OrderType, on_delete=DO_NOTHING)
    amount = models.DecimalField(decimal_places=10, max_digits=1000)
    price = models.DecimalField(decimal_places=10, max_digits=1000)
    avg_filling_price = models.DecimalField(decimal_places=10, max_digits=1000)
    fee = models.DecimalField(decimal_places=10, max_digits=1000)
    ts = models.DateTimeField()

    def __str__(self) -> str:
        return f'{self.user.username} - {self.pair} - {self.exchange} - {self.order_type} - {self.amount} - {self.price}'

    def save(self, *args, **kwargs):
        """
            Modify balance of user when transaction is made.
            Use atomic transaction to rollback if any error occurs.

            TODO: Send errors if quote balance has not enough founds to perform operation.
        """
        with transaction.atomic():
            quote = self.pair.quote
            total = self.amount * self.price
            quote_balance = Balance.objects.get_or_create(
                user=self.user, asset=quote, defaults={'amount': 0})[0]
            quote_balance.amount = quote_balance.amount - \
                Decimal(total + self.fee)
            quote_balance.save()

            base = self.pair.base
            base_balance = Balance.objects.get_or_create(
                user=self.user, asset=base, defaults={'amount': 0})[0]
            base_balance.amount = base_balance.amount + Decimal(self.amount)
            base_balance.save()
            super(Transaction, self).save(*args, **kwargs)


class TransactionSummary(Transaction):
    """
        Transaction summary, contains aggergated information about transactions
    """
    class Meta:
        """
            Meta class for TransactionSummary
        """
        proxy = True
        verbose_name = 'Transaction Summary'
        verbose_name_plural = 'Transactions Summary'
