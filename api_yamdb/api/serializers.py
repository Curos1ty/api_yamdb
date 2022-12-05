import datetime as dt

from django.db.models import Avg

from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий произведений."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров произведений."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор списка произведений."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title

    def get_rating(self, obj):
        """Вывод рейтинга произведения."""
        return obj.reviews.aggregate(Avg('score')).get('score__avg')


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и изменения произведений."""

    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(), many=False
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

    def validate_year(self, value):
        """Проверка года выпуска произведения."""
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                'Год выпуска не может превышать текущий год!'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title', )
        unique_together = ('author', 'title')

    def validate(self, attrs):
        request = self.context.get('request')
        title_id = self.context.get('view').kwargs.get('title_id')
        if request.method == 'POST' and Review.objects.filter(
            author=request.user, title=title_id
        ).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение!'
            )
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев к отзывам."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review', )
