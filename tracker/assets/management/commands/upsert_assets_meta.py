from django.core.management.base import BaseCommand
from django.conf import settings

from assets.models import Asset, Pair


class Command(BaseCommand):
    help = 'Crates assets and pairs based on settings'

    def handle(self, *args, **options):
        for asset in settings.ASSETS:
            print(f'Upsert asset: {asset}')
            Asset.objects.update_or_create(name=asset)

        all_assets = Asset.objects.all()

        for base in all_assets:
            for quote in all_assets:
                if base == quote:
                    continue
                print(f'Upsert pair: {base}-{quote}')
                Pair.objects.update_or_create(
                    name=f'{base}-{quote}', base=base, quote=quote)
