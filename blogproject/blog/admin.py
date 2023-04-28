from django.contrib import admin

from .models import Category, Comment, Post


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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Регистрация в админ-панели :model:`blog.Comment`.
    """

    list_display = ["author", "post", "pub_date"]
    list_filter = ["pub_date"]
