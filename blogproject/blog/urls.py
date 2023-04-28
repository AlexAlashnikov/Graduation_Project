from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="home"),
    path("post/<str:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("category_list/", views.CategoryListView.as_view(), name="category_list"),
    path("category/<int:pk>/<str:slug>/", views.PostByCategoryListView.as_view(), name="category_detail"),
]
