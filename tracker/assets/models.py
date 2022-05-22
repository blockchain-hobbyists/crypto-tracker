from django.db import models
from django.db.models.deletion import DO_NOTHING


class Asset(models.Model):
    """
        Asset model, contains information about asset
    """
    id = models.BigAutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=8, unique=True)

    def __str__(self) -> str:
        return f'{self.name}'


class Pair(models.Model):
    """
        BASE (asset to buy) - QUOTE (asset to pay)
    """
    id = models.BigAutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=10, unique=True)
    base = models.ForeignKey(
        Asset, on_delete=DO_NOTHING, related_name='base_id')
    quote = models.ForeignKey(
        Asset, on_delete=DO_NOTHING, related_name='quote_id')
    latest_price = models.DecimalField(
        decimal_places=10, max_digits=1000, null=True)

    def __str__(self) -> str:
        return self.name


class PairPrice(models.Model):
    """
        Pair price model, contains information about price of pair at a given time
    """
    id = models.BigAutoField(primary_key=True, editable=False)
    pair = models.ForeignKey(Pair, on_delete=DO_NOTHING)
    price = models.DecimalField(decimal_places=10, max_digits=1000)
    ts = models.DateTimeField()

    def __str__(self) -> str:
        return f'{self.pair} - {self.price} - {self.ts}'
