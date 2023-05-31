from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from attraction.models import Attraction, AttractionInfo, Comment, Ticket, TicketInfo
from system.models import ImageRelated
from utils.admin import CommonModelAdmin


class ImageInline(GenericTabularInline):
    model = ImageRelated
    extra = 1


class TicketInfoInline(admin.TabularInline):
    model = TicketInfo


class AttractionInfoInline(admin.TabularInline):
    model = AttractionInfo


@admin.register(Attraction)
class AttractionAdmin(CommonModelAdmin):
    list_display = ('name',  'rating', 'is_valid', 'is_popular', 'is_recommended', 'create_at', 'update_at')
    search_fields = ('name',)
    list_filter = ('is_valid', 'is_popular', 'is_recommended',)
    inlines = [ImageInline, AttractionInfoInline]


@admin.register(AttractionInfo)
class AttractionInfoAdmin(CommonModelAdmin):
    list_display = ('attraction', 'is_valid', 'create_at', 'update_at')
    search_fields = ('attraction__name',)
    list_filter = ('is_valid',)


@admin.register(Comment)
class CommentAdmin(CommonModelAdmin):
    list_display = ('user',  'attraction', 'is_valid', 'create_at', 'update_at')
    search_fields = ('attraction__name',)
    list_filter = ('is_valid',)
    inlines = [ImageInline]


@admin.register(Ticket)
class TicketAdmin(CommonModelAdmin):
    list_display = ('name',  'attraction', 'is_valid', 'create_at', 'update_at')
    search_fields = ('attraction__name', 'name')
    list_filter = ('is_valid',)
    inlines = [TicketInfoInline]


@admin.register(TicketInfo)
class TicketInfoAdmin(CommonModelAdmin):
    list_display = ('ticket', 'is_valid', 'create_at', 'update_at')
    search_fields = ('ticket__name',)
    list_filter = ('is_valid',)

