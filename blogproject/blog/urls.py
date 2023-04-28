from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="home"),
    path("post/create/", views.PostCreateView.as_view(), name="post_create"),
    path("post/<str:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("post/<str:slug>/update/", views.PostUpdateView.as_view(), name="post_update"),
    path("post/<str:slug>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
    path("post/<str:slug>/comment/", views.CommentCreateView.as_view(), name="comment_create"),
    path("post/<str:slug>/comment/<int:pk>/update/", views.CommentUpdateView.as_view(), name="comment_update"),
    path("post/<str:slug>/comment/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment_delete"),
    path("category_list/", views.CategoryListView.as_view(), name="category_list"),
    path("category/<int:pk>/<str:slug>/", views.PostByCategoryListView.as_view(), name="category_detail"),
    path("search/", views.PostSearchView.as_view(), name="search"),
]
