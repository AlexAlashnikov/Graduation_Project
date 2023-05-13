from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError

from .models import Profile


class ProfileUpdateForm(forms.ModelForm):
    """Форма обновления данных профиля :model:`user_profile.Profile`."""

    class Meta:
        model = Profile
        fields = ("bio", "profile_image", "date_birthday")

    def __init__(self, *args, **kwargs):
        """Обновление стилей формы обновления."""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})


class UserUpdateForm(forms.ModelForm):
    """Форма обновления данных пользователя :model:`auth.User`."""

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        """Обновление стилей формы обновления."""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})

    def clean_email(self):
        """Проверка email на уникальность."""
        email = self.cleaned_data.get("email")
        username = self.cleaned_data.get("username")
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError("Email адрес должен быть уникальным")
        return email


class UserRegisterForm(UserCreationForm):
    """Переопределенная форма регистрации пользователей :model:`auth.User`."""

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)

    def clean_email(self):
        """Проверка email на уникальность."""
        email = self.cleaned_data.get("email")
        username = self.cleaned_data.get("username")
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError("Email адрес должен быть уникальным")
        return email

    def __init__(self, *args, **kwargs):
        """Обновление стилей формы регистрации."""
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder": "Придумайте логин"})
        self.fields["email"].widget.attrs.update({"placeholder": "Введите ваш email"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Придумайте пароль"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Повторите пароль"})
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})


class UserLoginForm(AuthenticationForm):
    """Форма авторизации на сайте :model:`auth.User`."""

    def __init__(self, *args, **kwargs):
        """Обновление стилей формы регистрации."""
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "Введите ваш логин"
        self.fields["password"].widget.attrs["placeholder"] = "Введите ваш пароль"
        self.fields["username"].label = "Логин"
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})


class PasswordChangingForm(PasswordChangeForm):
    """Форма изменения пароля :model:`auth.User`."""

    class Meta:
        model = User
        fields = ("old_password", "new_password1", "new_password2")

    def clean(self):
        """Проверка пароля на уникальность."""
        clean_data = super().clean()
        user = self.user
        new = clean_data.get("new_password1")
        if user.check_password(new):
            raise ValidationError("Новый пароль совпадает со старым!")
        else:
            return clean_data

    def __init__(self, *args, **kwargs):
        """Обновление стилей формы"""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})
