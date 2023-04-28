from django import template

from blog.models import Post, Comment

register = template.Library()


@register.simple_tag
def total_post():
    """
    :model:`blog.Post`.

    Returns:
        Колличество всех постов.
    """
    return Post.objects.all().count()


@register.inclusion_tag("comment/last_comments.html")
def show_latest_comments(count=5):
    """
    :model:`blog.Comment`.

    Returns:
        Последние 5 комментариев.
    """
    latest_comments = Comment.objects.all().order_by("-pub_date").select_related("author")[:count]
    return {"latest_comments": latest_comments}
