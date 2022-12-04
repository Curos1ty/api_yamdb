import datetime as dt

from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment


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
        rating = obj.reviews.aggregate(Avg('score')).get('score__avg')
        if not rating:
            return None
        return rating


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
    # author = serializers.SlugRelatedField(
    #          read_only=True, slug_field='username'
    # )
    author = serializers.IntegerField(default=1, read_only=True)

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title', )


class CommentSerializer(serializers.ModelSerializer):
    # author = serializers.SlugRelatedField(
    #          read_only=True, slug_field='username'
    # )
    author = serializers.IntegerField(default=1, read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review', )
