import factory
from factory.django import DjangoModelFactory

from posts.models import Post
from users.factories import UserFactory


class PostFactory(DjangoModelFactory):
    author = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda x: f'Title {x}')
    content = factory.Sequence(lambda x: f'Content of Title {x}')

    class Meta:
        model = Post
