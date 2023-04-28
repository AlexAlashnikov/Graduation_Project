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
    Представление профиля пользователя.
    """

    model = Profile
    context_object_name = "profile"
    template_name = "user_profile/profile_detail.html"

    def get_context_data(self, **kwargs):
        """
        Получить контекст для этого представления.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = f"Страница пользователя: {self.object.user.username}"
        context["all_posts_user"] = Post.objects.filter(author=self.object.user)
        return context


class FollowingProfileCreateView(View):
    model = Profile

    def post(self, request, **kwargs):
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
    Представление для редактирования профиля пользователя.
    """

    model = Profile
    form_class = ProfileUpdateForm
    template_name = "user_profile/update_profile.html"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        """
        Получить контекст для этого представления.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = f"Редактирование профиля пользователя: {self.request.user.username}"
        if self.request.POST:
            context["user_form"] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context["user_form"] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
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
    Представление регистрации на сайте с формой регистрации.
    """

    form_class = UserRegisterForm
    success_url = reverse_lazy("profile:login")
    template_name = "authenticated/register_user.html"
    success_message = "Регистрация прошла успешно!"

    def get_context_data(self, **kwargs):
        """
        Получить контекст для этого представления.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация на сайте"
        return context


class UserLoginView(SuccessMessageMixin, LoginView):
    """
    Авторизация на сайте.
    """

    form_class = UserLoginForm
    template_name = "authenticated/login.html"
    next_page = "blog:home"
    success_message = "Добро пожаловать!"

    def get_context_data(self, **kwargs):
        """
        Получить контекст для этого представления.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Авторизация на сайте"
        return context


class UserLogoutView(LogoutView):
    """
    Выход с сайта.
    """

    next_page = "blog:home"


class CustomPasswordChangeView(PasswordChangeView):
    """
    Изменение пароля пользователя
    """

    form_class = PasswordChangingForm
    template_name = "authenticated/password_change.html"
    success_url = reverse_lazy("profile:login")

    def form_valid(self, form):
        form.save()
        self.request.session.flush()
        logout(self.request)
        messages.success(self.request, "Ваш пароль успешно изменен!!!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Получить контекст для этого представления.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Смена Пароля"
        return context
