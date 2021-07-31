from django.contrib import admin
from .models import Asset, Location, Event ,FileUplaod


# class AssetInline(admin.StackedInline): # new
#     model = Asset
#
#
# class LocationAdmin(admin.ModelAdmin): # new
#     inlines = [
#         AssetInline,
#     ]


# class LocationsInline(admin.StackedInline): # new
#     model = Location
#
#
# class EventAdmin(admin.ModelAdmin): # new
#     inlines = [
#         LocationsInline,
#     ]

admin.site.register(FileUplaod)
admin.site.register(Asset)
admin.site.register(Location)
admin.site.register(Event)



