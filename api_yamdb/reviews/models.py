from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User

from .validators import validate_year


class Category(models.Model):
    """Категории произведений."""

    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField('Слаг категории', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры произведений."""

    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField('Слаг жанра', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения."""

    name = models.CharField('Название произведения', max_length=256)
    year = models.PositiveSmallIntegerField(
        'Год выпуска произведения',
        validators=[validate_year]
    )
    description = models.TextField('Описание произведения', blank=True)
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзывы."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Заголовок'
    )
    text = models.TextField('Отзыв')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Комментарии."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField('Комментарий')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name_plural = 'Комменты'
        verbose_name = 'Коммент'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text
