from django.core.management.base import BaseCommand

from django.contrib.auth import get_user_model
from django.conf import settings
from assets.models import Asset

from users.models import Balance


class Command(BaseCommand):
    """
        Userts Exchange data based on settings.EXCHANGES
    """
    help = ''

    def handle(self, *args, **options):
        """
            Create empty balances for all users and assets
        """
        assets = settings.ASSETS
        for user in get_user_model().objects.all():
            for asset in assets:
                asset_obj = Asset.objects.get(name=asset)
                try:
                    Balance.objects.get(user=user, asset=asset_obj)
                except Balance.DoesNotExist:
                    print(
                        f'Create balance for user: {user.username} and asset: {asset}')
                    Balance.objects.create(
                        user=user,
                        asset=asset_obj,
                        amount=0
                    )
