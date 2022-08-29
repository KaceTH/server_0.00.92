from django.db import models
from Account.models import User,TimeStampedModel

# Create your models here.


class PostingModel(TimeStampedModel) :
    likes = models.ManyToManyField(User, blank=True)
    text = models.TextField(blank=True)

    class Meta:
        abstract = True


class Post(PostingModel) :

    FORMAT_CHOICES = (
        (1, 'Free writing'),
        (2, 'Suggestion'),
        (3, 'Notice'),
    )

    author = models.ForeignKey(
        User,
        blank = True,
        null=True,
        on_delete = models.DO_NOTHING,
        related_name = 'post_author'
    )

    format = models.IntegerField(
        choices=FORMAT_CHOICES, blank=True, default=1
    )
    title = models.CharField(max_length=150, blank=True, default='Unnamed post')

    def __str__(self):
        return self.title