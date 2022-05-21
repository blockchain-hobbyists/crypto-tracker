from django.contrib import admin
from admin_auto_filters.filters import AutocompleteFilter
from .models import Profile, Balance


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


class AssetFilter(AutocompleteFilter):
    """
        Asset filter searches for base and quote names
    """
    title = 'Asset'
    field_name = 'asset'


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    """
        Admin panel for balances. allow filtering by username and asset name
    """
    list_display = ('user', 'asset', 'amount')
    list_filter = ['user', AssetFilter]
