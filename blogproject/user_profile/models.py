from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse

from blog.utils import unique_slugify


class Profile(models.Model):
    """
    Хранит записи профилей,
    связанную с :model:`auth.User`.
    """

    user = models.OneToOneField(User, verbose_name="Профиль пользователя", on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self", verbose_name="Подписки", related_name="followed_by", symmetrical=False, blank=True
    )
    slug = models.SlugField(verbose_name="Персональная ссылка", max_length=255, blank=True, unique=True)
    bio = models.TextField(max_length=500, verbose_name="Информация о себе", blank=True)
    date_birthday = models.DateField(verbose_name="Дата рождения", blank=True, null=True)
    profile_image = models.ImageField(
        null=True,
        blank=True,
        upload_to="user_profile/media/user_image",
        validators=[FileExtensionValidator(allowed_extensions=["png", "jpg", "webp", "jpeg"])],
    )

    def __str__(self):
        """Возвращает строку в виде имени пользователя."""
        return self.user.username

    def save(self, *args, **kwargs):
        """Создание поля slug при его отсутствии."""
        if not self.slug:
            self.slug = unique_slugify(self, self.user.username)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Возвращает ссылку на профиль, по идентификатору slug."""
        return reverse("profile:profile_detail", kwargs={"slug": self.slug})

    @property
    def get_profile_image(self):
        """Получение заглушки при отсутсвии изображения."""
        if not self.profile_image:
            return "/static/img/default-avatar.png"
        return self.profile_image.url

    @property
    def get_age(self):
        """Возвращает возраст пользователя."""
        return (date.today() - self.date_birthday) // timedelta(days=365.2425)
