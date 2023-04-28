from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CommentCreateForm, PostCreateForm
from .mixins import AuthorRequiredMixin
from .models import Category, Comment, Post


class PostDetailView(DetailView):
    """
    Отображение отдельного объекта :model:`blog.Post`.

    **Context Object Name**

    ``post``
        Экземпляр :model:`blog.Post` по идентификатору `slug`.

    **Template:**

    :template:`blog/post_detail.html`
    """

    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        """
        Вернуть элемент для этого представления по идентификатору `slug`.
        """
        return (
            Post.objects.filter(slug=self.kwargs["slug"])
            .select_related("author", "category")
            .prefetch_related("comments__author", "author__profile")
        )

    def get_context_data(self, **kwargs):
        """
        Получить контекст для этого представления.
        """
        context = super().get_context_data(**kwargs)
        liked = False
        if self.object.likes.filter(id=self.request.user.id).exists():
            liked = True
        context["total_likes"] = self.object.total_likes()
        context["title"] = self.object.title
        context["liked"] = liked
        return context


class PostListView(ListView):
    """
    Отображение списка объектов :model:`blog.Post`.

    **Context Object Name**

    ``posts``
        Экземпляр :model:`blog.Post`.

    **Template:**

    :template:`blog/post_list.html`
    """

    queryset = Post.objects.all().order_by("-post_date").select_related("category").prefetch_related("author__profile")
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """
        Получить контекст для этого представления.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        return context


class PostByCategoryListView(ListView):
    """
    Отображение списка объектов :model:`blog.Post`,
    связанную с :model:`blog.Category`.

    **Context Object Name**

    ``posts``
        Экземпляр :model:`blog.Post`.

    **Template:**

    :template:`category/category_detail.html`
    """

    model = Post
    template_name = "category/category_detail.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        """
        Вернуть список элементов для этого представления.
        """
        self.category = Category.objects.get(pk=self.kwargs["pk"])
        queryset = self.model.objects.all().filter(category_id=self.category.id).prefetch_related("author__profile")
        return queryset

    def get_context_data(self, **kwargs):
        """
        Получить контекст для этого представления.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = self.category.name
        return context


class CategoryListView(ListView):
    """
    Отображение списка объектов :model:`blog.Category`.

    **Context Object Name**

    ``categories``
        Экземпляр :model:`blog.Category`.

    **Template:**

    :template:`category/category_list.html`
    """

    model = Category
    template_name = "category/category_list.html"
    context_object_name = "categories"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        """
        Получить контекст для этого представления.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Категории"
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Создание объекта :model:`blog.Post`.

    **Template:**

    :template:`blog/post_create.html`
    """

    model = Post
    template_name = "blog/post_create.html"
    form_class = PostCreateForm
    login_url = "profile:login"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Получить контекст для этого представления.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление поста"
        return context


class PostUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Обновление объекта :model:`blog.Post`.

    **Context Object Name**

    ``post``
        Экземпляр :model:`blog.Post`.

    **Template:**

    :template:`blog/post_update.html`
    """

    model = Post
    template_name = "blog/post_update.html"
    context_object_name = "post"
    form_class = PostCreateForm
    login_url = "blog:home"
    success_message = "Вы успешно обновили пост."

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Получить контекст для этого представления.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = f"Обновление поста: {self.object.title}"
        return context


class PostDeleteView(AuthorRequiredMixin, DeleteView):
    """
    Удаление объекта :model:`blog.Post`.

    **Context Object Name**

    ``post``
        Экземпляр :model:`blog.Post`.

    **Template:**

    :template:`blog/post_delete.html`
    """

    model = Post
    success_url = reverse_lazy("blog:home")
    context_object_name = "post"
    template_name = "blog/post_delete.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Получить контекст для этого представления.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = f"Удаление поста: {self.object.title}"
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Создание объекта :model:`blog.Comment`.

    **Template:**

    :template:`comment/comment_create.html`
    """

    template_name = "comment/comment_create.html"
    form_class = CommentCreateForm
    login_url = "profile:login"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(slug=self.kwargs["slug"])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Получить контекст для этого представления.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавления комментария"
        return context


class CommentUpdateView(AuthorRequiredMixin, UpdateView):
    """
    Обновление объекта :model:`blog.Comment`.

    **Context Object Name**

    ``comment``
        Экземпляр :model:`blog.Comment`.

    **Template:**

    :template:`comment/comment_update.html`
    """

    model = Comment
    context_object_name = "comment"
    template_name = "comment/comment_update.html"
    form_class = CommentCreateForm

    def get_context_data(self, **kwargs):
        """
        Получить контекст для этого представления.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = f"Обновление комментария: {self.object.text}"
        return context


class CommentDeleteView(AuthorRequiredMixin, DeleteView):
    """
    Удаление объекта :model:`blog.Comment`.

    **Context Object Name**

    ``comment``
        Экземпляр :model:`blog.Comment`.

    **Template:**

    :template:`comment/comment_delete.html`
    """

    model = Comment
    context_object_name = "comment"
    template_name = "comment/comment_delete.html"
    success_url = reverse_lazy("blog:home")

    def get_context_data(self, **kwargs):
        """
        Получить контекст для этого представления.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = f"Удаление комментария: {self.object.text}"
        return context
