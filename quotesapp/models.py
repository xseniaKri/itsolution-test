from django.conf import settings
from django.db import models


class Source(models.Model):
    category = models.CharField(
        max_length=255, help_text="Введите категорию (книга, фильм и т. д.)"
    )
    name = models.CharField(
        max_length=255, help_text="Введите название источника (напр. Властелин колец)"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["category", "name"], name="unique_category_name"
            ),
        ]


class Quote(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name="quotes")
    text = models.CharField(
        max_length=255,
        help_text="Введите цитату (напр. Быть или не быть - вот, в чем вопрос)",
        unique=True,
    )
    weight = models.PositiveIntegerField(
        default=1, help_text="Введите вес цитаты (от 1 до 10)"
    )
    views = models.PositiveIntegerField(default=0)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quotes"
    )

    def likes_count(self):
        return self.votes.filter(value=1).count()  # type: ignore

    def dislikes_count(self):
        return self.votes.filter(value=-1).count()  # type: ignore


class Favourites(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="liked_by")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favourites"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["quote", "owner"], name="unique_quotes_owner"
            )
        ]


class Vote(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="votes"
    )
    value = models.SmallIntegerField(choices=[(-1, "Dislike"), (1, "Like")])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["quote", "user"], name="unique_quote_user"),
        ]
