from django.core.management.base import BaseCommand

from django.conf import settings

from transactions.models import Exchange, OrderType


class Command(BaseCommand):
    """
        Userts Exchange data based on settings.EXCHANGES
    """
    help = ''

    def handle(self, *args, **options):
        exchanges = settings.EXCHANGES
        for exchange, order_types in exchanges:
            print(f'Upsert exchange: {exchange}')
            Exchange.objects.update_or_create(name=exchange)
            for order_type in order_types:
                print(f'Upsert order type: {order_type}')
                OrderType.objects.update_or_create(name=order_type)
