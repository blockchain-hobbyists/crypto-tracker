from django.test import TestCase
from assets.management.commands.upsert_assets_meta import Command as UpsertAMeta
from assets.models import Pair


class AssetTestCase(TestCase):
    """
        Test Asset related functionality
    """

    @classmethod
    def setUpTestData(cls):
        UpsertAMeta().handle()

    def test_eur_btc_pair_exists(self):
        """
            Test that EUR-BTC / BTC-EUR pairs exists
        """
        self.assertTrue(Pair.objects.filter(
            base__name='EUR',
            quote__name='BTC').exists())
        self.assertTrue(Pair.objects.filter(
            base__name='BTC',
            quote__name='EUR').exists())
