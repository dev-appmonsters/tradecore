from django.db import models

from django.conf import settings


class Post(models.Model):

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    title = models.CharField(max_length=150)

    content = models.TextField()

    posted_on = models.DateTimeField(
        auto_now_add=True,
    )

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_posts",
        blank=True,
    )

    def __str__(self):
        return '"{title}" by {author}'.format(
            title=self.title,
            author=self.author,
        )
