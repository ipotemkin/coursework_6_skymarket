from django.conf import settings
from django.db import models

from skymarket.settings import MEDIA_ROOT
from users.models import User


class Ad(models.Model):
    image = models.ImageField(upload_to="images/", null=True, verbose_name="Фото")
    title = models.CharField(
        max_length=200,
        # validators=[MinLengthValidator(10)],
        verbose_name="Название товара"
    )
    price = models.PositiveIntegerField(verbose_name="Цена товара")
    description = models.CharField(max_length=1000, verbose_name="Описание товара", null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True)

    # is_published = models.BooleanField(default=False, verbose_name="Опубликован или нет")
    # category = models.ForeignKey(Cat, on_delete=models.PROTECT, verbose_name="Категория")

    class Meta:
        verbose_name_plural = "Объявления"
        verbose_name = "Объявление"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length=1000, verbose_name="Текст отзыва", null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name="Объявление")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Отзывы"
        verbose_name = "Отзыв"
        # ordering = ["-created_at"]

    def __str__(self):
        return self.text[:20]


ADO = Ad.objects  # noqa
COMO = Comment.objects  # noqa
# USERO = User.objects  # noqa
# LOCO = Location.objects  # noqa
# SELO = Selection.objects # noqa
