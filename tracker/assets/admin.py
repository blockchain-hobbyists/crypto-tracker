from django.contrib import admin
from .models import Pair, Asset, PairPrice


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Pair)
class PairAdmin(admin.ModelAdmin):
    search_fields = ['name', ]


@admin.register(PairPrice)
class PairPriceAdmin(admin.ModelAdmin):
    search_fields = ['pair__name']
