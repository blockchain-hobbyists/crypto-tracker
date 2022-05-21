from django.core.management.base import BaseCommand

from assets.management.commands.upsert_assets_meta import Command as UpsertAssetsMetaCommand
from users.management.commands.upsert_users_meta import Command as UpsertUsersMetaCommand
from transactions.management.commands.upsert_transactions_meta import Command as UpsertTransactionsMetaCommand


class Command(BaseCommand):
    """
        Upsert all meta based on settings
    """
    help = 'Upserts all meta to db, individual commands can be run with upsert_[app]_meta'

    def handle(self, *args, **options):
        UpsertAssetsMetaCommand().handle()
        UpsertUsersMetaCommand().handle()
        UpsertTransactionsMetaCommand().handle()
