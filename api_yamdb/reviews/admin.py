from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('title', 'text')
    list_filter = ('pub_date', )
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'category')
    search_fields = ('name', 'description')
    list_filter = ('year', )
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'text', 'author', 'pub_date')
    search_fields = ('text', )
    list_filter = ('pub_date', )
    empty_value_display = '-пусто-'


admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
