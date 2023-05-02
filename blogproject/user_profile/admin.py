from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Регистрация в админ-панели :model:`user_profile.Profile`."""

    list_display = ["user"]
