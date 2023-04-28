from django.urls import path

from . import views

app_name = "profile"

urlpatterns = [
    path("profile_detail/<str:slug>/", views.ProfileView.as_view(), name="profile_detail"),
]
