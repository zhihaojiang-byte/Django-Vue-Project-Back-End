from django.contrib import admin


class CommonModelAdmin(admin.ModelAdmin):
    list_per_page = 10

    actions = ['activate_selected_items', 'deactivate_selected_items']

    def deactivate_selected_items(self, request, queryset):
        queryset.update(is_valid=False)

    def activate_selected_items(self, request, queryset):
        queryset.update(is_valid=True)

