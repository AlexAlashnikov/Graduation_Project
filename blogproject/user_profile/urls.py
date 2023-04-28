from django.urls import path

from . import views

app_name = "profile"

urlpatterns = [
    path("profile_detail/<str:slug>/", views.ProfileView.as_view(), name="profile_detail"),
    path("update_profile/", views.ProfileEditView.as_view(), name="update_profile"),
    path("register/", views.RegisterCreateView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("change_pass/", views.CustomPasswordChangeView.as_view(), name="password_change"),
]
