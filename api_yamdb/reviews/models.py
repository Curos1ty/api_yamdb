from django.db import models

from .validators import validate_year, validate_score
# from users.models import User


class Category(models.Model):
    """Категории произведений."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения."""
    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField(validators=[validate_year])
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category,
        related_name='categories',
        on_delete=models.SET_NULL,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genres'
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзывы."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(verbose_name='Отзыв')
    # добавить после создания Модели Юзера и удалить временное поле
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     verbose_name='Автор',
    #     related_name='reviews'
    # )
    author = models.IntegerField()
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[validate_score]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Комментарии."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='отзыв',
        related_name='comments'
    )
    text = models.TextField(verbose_name='Комментарий')
    # добавить после создания Модели Юзера и удалить временное поле
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='comments'
    # )
    author = models.IntegerField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name_plural = 'Комменты'
        verbose_name = 'Коммент'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text
