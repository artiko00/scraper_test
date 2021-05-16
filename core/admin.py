from django.contrib import admin
from core.models import Asset, Scraper, AssetData

admin.site.register(Asset)
admin.site.register(Scraper)
admin.site.register(AssetData)