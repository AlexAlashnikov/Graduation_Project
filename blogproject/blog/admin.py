from django.contrib import admin

from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Регистрация в админ-панели :model:`blog.Category`.
    """

    list_display = ["name", "post_amount", "slug"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Регистрация в админ-панели :model:`blog.Post`.
    """

    list_display = ["title", "author", "slug", "category"]
    list_display_links = ("title", "slug")
