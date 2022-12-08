from django.shortcuts import get_object_or_404

from reviews.models import Review, Title


def get_title_or_review(self):
    """Получение title_id или review_id."""
    if 'review_id' in self.kwargs:
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review
    title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
    return title
