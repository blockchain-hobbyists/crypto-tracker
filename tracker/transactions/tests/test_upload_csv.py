import os

from django.test import TestCase
from django.contrib.auth.models import User
from django.core import management


file = os.path.join(os.path.dirname(__file__), 'example.csv')


class TransactionTestCase(TestCase):
    """
        Test the csv upload of transactions
    """
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        management.call_command('upsert_all_meta')

    def test_upload_csv(self):
        management.call_command('upload_transactions_csv', '--path', file)
