from django.db import models

from .validators import validate_year
# from users.models import User


class Category(models.Model):
    """Категории произведений."""
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField('Слаг категории', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField('Слаг жанра', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

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
        through='GenreTitle',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзывы."""
    SCORE_CHOICES = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),
                     (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')]
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
    #     verbose_name='Автор',
    #     on_delete=models.CASCADE,
    #     related_name='reviews'
    #     unique=True
    # )
    author = models.IntegerField(blank=True)
    # score = models.IntegerField(
    #     'Оценка',
    #     validators=[validate_score]
    # )
    score = models.PositiveSmallIntegerField('Оценка', choices=SCORE_CHOICES)
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
    #     verbose_name='Автор',
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


class GenreTitle(models.Model):
    """Промежуточная модель для связи отношения ManyToMany."""
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.genre
