from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class AuthorRequiredMixin(AccessMixin):
    """Проверяет что текущий пользователь аутентифицирован."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_authenticated:
            if request.user != self.get_object().author:
                messages.info(request, "Редактирование и удаление доступно только автору.")
                return redirect("blog:home")
        return super().dispatch(request, *args, **kwargs)
