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
                print(
                    f'Create balance for user: {user.username} and asset: {asset}')
                Balance.objects.update_or_create(
                    user=user, asset=Asset.objects.get(name=asset), amount=0)
