from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings
from assets.models import Pair
from assets.coinmarketcap import get_pair_price
import time


class Command(BaseCommand):
    """
        Updateds Asset Pair prices, save price to Asset.latest_price too
    """
    help = ''

    INFINITE_LOOP_SLEEP = 60

    def add_arguments(self, parser):
        parser.add_argument('--infinite-run', action='store_true',
                            help='Run command in an infinite loop')

    def handle(self, *args, **options):
        if options['infinite_run']:
            while True:
                time.sleep(self.INFINITE_LOOP_SLEEP)
                self._update_pairs()
        else:
            self._update_pairs()

    def _update_pairs(self):
        with transaction.atomic():
            pairs = Pair.objects.filter(
                quote__name=settings.COINMARKETCAP['QUOTE'],
                base__name__in=settings.COINMARKETCAP['BASES'])
            for pair in pairs:
                pair_price = get_pair_price(pair)
                pair_price.save()

                pair.latest_price = pair_price.price
                pair.save(update_fields=['latest_price'])
                self.stdout.write(self.style.SUCCESS(
                    f'Lastest price of {pair} is: {pair.latest_price}'))
