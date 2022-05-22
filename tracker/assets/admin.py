from django.contrib import admin
from .models import Pair, Asset, PairPrice


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    """
        Asset admin panel
    """
    search_fields = ['name']


@admin.register(Pair)
class PairAdmin(admin.ModelAdmin):
    """
        Pair admin panel
    """
    search_fields = ['name', ]


@admin.register(PairPrice)
class PairPriceAdmin(admin.ModelAdmin):
    """
        PairPrice admin panel
    """
    search_fields = ['pair__name']
