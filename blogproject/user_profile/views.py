from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, View

from blog.models import Post

from .forms import PasswordChangingForm, ProfileUpdateForm, UserLoginForm, UserRegisterForm, UserUpdateForm
from .models import Profile


class ProfileView(DetailView):
    """
    Отображение отдельного объекта :model:`user_profile.Profile`.

    **Context Object Name**

    ``profile``
        Экземпляр :model:`user_profile.Profile`.

    **Template:**

    :template:`user_profile/profile_detail.html`
    """

    model = Profile
    context_object_name = "profile"
    template_name = "user_profile/profile_detail.html"

    def get_context_data(self, **kwargs):
        """Получить контекст для этого представления."""
        context = super().get_context_data(**kwargs)
        context["title"] = f"Страница пользователя: {self.object.user.username}"
        context["all_posts_user"] = Post.objects.filter(author=self.object.user)
        return context


class FollowingProfileCreateView(View):
    """
    Создание объекта follows :model:`user_profile.Profile`.
    """

    model = Profile

    def post(self, request, **kwargs):
        """
        Получение объекта :model:`user_profile.Profile`
        по идентификатору `slug`.

        Returns:
            redirect: URL адрес объекта :model:`user_profile.Profile`
        """
        if request.user.is_authenticated:
            profile = self.model.objects.get(slug=self.kwargs["slug"])
            curent_user_profile = request.user.profile
            if curent_user_profile in profile.follows.all():
                profile.follows.remove(curent_user_profile)
            else:
                profile.follows.add(curent_user_profile)
        return redirect(profile)


class ProfileEditView(UpdateView):
    """
    Обновление объекта :model:`user_profile.Profile`.

    **Template:**

    :template:`user_profile/update_profile.html`
    """

    model = Profile
    form_class = ProfileUpdateForm
    template_name = "user_profile/update_profile.html"

    def get_object(self, queryset=None):
        """Получение экземпляра :model:`user_profile.Profile`."""
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        """Получить контекст для этого представления."""
        context = super().get_context_data(**kwargs)
        context["title"] = f"Редактирование профиля пользователя: {self.request.user.username}"
        if self.request.POST:
            context["user_form"] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context["user_form"] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        """
        Проверка формы
        для корректного сохранения данных в :model:`user_profile.Profile`.
        """
        context = self.get_context_data()
        user_form = context["user_form"]
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({"user_form": user_form})
                return self.render_to_response(context)
        return super(ProfileEditView, self).form_valid(form)


class RegisterCreateView(SuccessMessageMixin, CreateView):
    """
    Создание объекта :model:`auth.User`.

    **Template:**

    :template:`authenticated/register_user.html`
    """

    form_class = UserRegisterForm
    success_url = reverse_lazy("profile:login")
    template_name = "authenticated/register_user.html"
    success_message = "Регистрация прошла успешно!"

    def get_context_data(self, **kwargs):
        """Получить контекст для этого представления."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация на сайте"
        return context


class UserLoginView(SuccessMessageMixin, LoginView):
    """
    Авторизация объекта :model:`auth.User`.

    **Template:**

    :template:`authenticated/login.html`
    """

    form_class = UserLoginForm
    template_name = "authenticated/login.html"
    next_page = "blog:home"
    success_message = "Добро пожаловать!"

    def get_context_data(self, **kwargs):
        """Получить контекст для этого представления."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Авторизация на сайте"
        return context


class UserLogoutView(LogoutView):
    """Выход из системы."""

    next_page = "blog:home"


class CustomPasswordChangeView(PasswordChangeView):
    """
    Изменение пароля экземпляра :model:`auth.User`.

    **Template:**

    :template:`authenticated/password_change.html`
    """

    form_class = PasswordChangingForm
    template_name = "authenticated/password_change.html"
    success_url = reverse_lazy("profile:login")

    def form_valid(self, form):
        """
        Проверка формы
        для корректного сохранения данных, с выходом из сессии.
        """
        form.save()
        self.request.session.flush()
        logout(self.request)
        messages.success(self.request, "Ваш пароль успешно изменен!!!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Получить контекст для этого представления."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Смена Пароля"
        return context
