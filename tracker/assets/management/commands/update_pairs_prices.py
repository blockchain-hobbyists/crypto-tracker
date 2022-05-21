from django.core.management.base import BaseCommand
from assets.models import Asset, Pair


class Command(BaseCommand):
    """
        Updateds Asset Pair prices, save price to Asset.latest_price too
    """
    help = ''

    def handle(self, *args, **options):
        pass
