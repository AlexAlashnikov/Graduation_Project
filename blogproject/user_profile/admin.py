from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Админ-панель модели Profile.
    """

    list_display = ["user"]
