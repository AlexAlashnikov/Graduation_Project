from django.views.generic import DetailView

from blog.models import Post

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
