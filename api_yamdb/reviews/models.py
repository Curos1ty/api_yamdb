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
        related_name='reviews',
        verbose_name='Заголовок'
    )
    text = models.TextField('Отзыв')
    # добавить после создания Модели Юзера и удалить временное поле
    # author = models.ForeignKey(
    #     User,
    #     'Автор',
    #     on_delete=models.CASCADE,
    #     related_name='reviews'
    # )
    author = models.IntegerField()
    score = models.IntegerField(
        'Оценка',
        validators=[validate_score]
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
    # добавить после создания Модели Юзера и удалить временное поле
    # author = models.ForeignKey(
    #     User,
    #     'Автор',
    #     on_delete=models.CASCADE,
    #     related_name='comments'
    # )
    author = models.IntegerField()
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
