from django.contrib import admin
from .models import Pair, Asset


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Pair)
class PairAdmin(admin.ModelAdmin):
    search_fields = ['base__name', 'quote__name', ]
