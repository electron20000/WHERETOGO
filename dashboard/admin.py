from django.contrib import admin

from .models import Announcement, AppearanceSetting, Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order", "is_closed", "updated_at")
    list_editable = ("order", "is_closed")
    ordering = ("order",)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("text", "location", "is_active", "is_important", "updated_at")
    list_filter = ("location", "is_active", "is_important")
    search_fields = ("text",)


@admin.register(AppearanceSetting)
class AppearanceSettingAdmin(admin.ModelAdmin):
    list_display = ("key", "updated_at")
