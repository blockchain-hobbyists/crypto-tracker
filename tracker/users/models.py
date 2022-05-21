from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User


class Profile(models.Model):
    """
        Profile of user, contains additional info about user such as wallets owned
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        default='default.jpg', upload_to='profile_images')

    def __str__(self):
        return self.user.username


class Balance(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    asset = models.ForeignKey('assets.Asset', on_delete=CASCADE)
    amount = models.DecimalField(decimal_places=10, max_digits=1000)

    def __str__(self):
        return f'{self.user.username} - {self.asset.name}'

    class Meta:
        unique_together = ('user', 'asset')
