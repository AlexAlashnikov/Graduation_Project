from django import forms

from .models import Comment, Post


class PostCreateForm(forms.ModelForm):
    """Форма создания объекта :model:`blog.Post`."""

    class Meta:
        model = Post
        fields = (
            "title",
            "category",
            "short_description",
            "body",
            "slug",
            "image",
        )

    def __init__(self, *args, **kwargs):
        """Обновление стилей формы."""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})
            self.fields["title"].widget.attrs.update({"placeholder": "Заголовок статьи"})
            self.fields["slug"].widget.attrs.update({"placeholder": "Ссылка статьи (необязательно)"})
            self.fields["short_description"].widget.attrs.update(
                {"placeholder": "Введите небольшое описание в 300 символов"}
            )
            self.fields["category"].empty_label = "Выберите категорию"
            self.fields["body"].widget.attrs.update({"class": "form-control django-ckeditor-widget ckeditor"})


class CommentCreateForm(forms.ModelForm):
    """Форма создания объекта :model:`blog.Comment`."""

    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control", "placeholder": "Комментарий"}),
        }
