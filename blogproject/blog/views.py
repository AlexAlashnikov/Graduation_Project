from django.views.generic import DetailView, ListView

from .models import Category, Post


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
