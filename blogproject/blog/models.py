from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse

from .utils import unique_slugify


class Category(models.Model):
    """
    Хранит записи категорий.
    """

    name = models.CharField(verbose_name="Название категории", max_length=100)
    slug = models.SlugField(max_length=200, blank=True)
    description = models.TextField(verbose_name="Описание категории", max_length=300)
    post_amount = models.IntegerField(default=0)

    def __str__(self) -> str:
        """
        Возвращает строку в виде названия категории в админ панели.
        """
        return self.name

    def save(self, *args, **kwargs):
        """
        Создание поля slug при его отсутствии.
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    """
    Хранит записи постов,
    связанную с :model:`Category` и :model:`auth.User`.
    """

    title = models.CharField(verbose_name="Заголовок", max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_post", verbose_name="Автор")
    short_description = models.TextField(max_length=300, verbose_name="Краткое описание", null=True)
    body = RichTextField(verbose_name="Описание")
    slug = models.SlugField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    post_date = models.DateTimeField(verbose_name="Дата добавления", auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="post_likes")
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to="blog/media/post_image",
        validators=[FileExtensionValidator(allowed_extensions=["png", "jpg", "webp", "jpeg"])],
    )

    def __str__(self) -> str:
        """
        Возвращает строку в виде заголовка статьи в админ панели.
        """
        return self.title

    def save(self, *args, **kwargs):
        """
        Создание поля slug при его отсутствии.
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Ссылка поста, по slug полю.
        """
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    def total_likes(self):
        return self.likes.count()

    @property
    def get_thumbnail(self):
        """
        Получение заглушки при отсутсвии изображения.
        """
        if not self.image:
            return "/static/img/placeholder.png"
        return self.image.url


class Comment(models.Model):
    """
    Хранит записи комментариев,
    связанную с :model:`Post` и :model:`auth.User`.
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост", related_name="comments")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор комментария", related_name="comments_author"
    )
    text = models.TextField(verbose_name="Текст комментария", max_length=1500)
    pub_date = models.DateTimeField(verbose_name="Дата добавления", auto_now_add=True)

    def __str__(self) -> str:
        """
        Возвращает строку в виде автора комментария и заголовок поста в амин панели.
        """
        return f"{self.author} {self.post.title}"

    def get_absolute_url(self):
        """
        Ссылка поста, по slug полю.
        """
        return reverse("blog:post_detail", kwargs={"slug": self.post.slug})
