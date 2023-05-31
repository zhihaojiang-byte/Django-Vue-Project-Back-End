from django.contrib import admin

from system.models import Swipe, ImageRelated
from utils.admin import CommonModelAdmin


@admin.register(Swipe)
class SwipeAdmin(CommonModelAdmin):
    list_display = ('name', 'order', 'is_valid', 'create_at', 'update_at')
    search_fields = ('name',)
    list_filter = ('is_valid',)


@admin.register(ImageRelated)
class ImageRelated(CommonModelAdmin):
    list_display = ('name', 'img', 'is_valid', 'create_at', 'update_at')
    search_fields = ('name',)
    list_filter = ('is_valid',)

