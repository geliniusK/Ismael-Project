from django.contrib import admin

from .models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = ['description', 'author', 'pub_time']


admin.site.register(Item, ItemAdmin)
# Register your models here.
