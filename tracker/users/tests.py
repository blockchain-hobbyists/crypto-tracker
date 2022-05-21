from django.test import TestCase

from users.models import Profile, User


class TransactionTestCase(TestCase):

    def test_profile(self):
        user = User.objects.create_superuser(
            'myuser', 'myemail@test.com', 'password')
        profile = Profile.objects.create(user=user)
        self.assertEqual(profile.user, user)
