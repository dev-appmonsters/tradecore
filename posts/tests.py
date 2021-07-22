from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework_simplejwt.tokens import RefreshToken

from posts.factories import PostFactory
from posts.models import Post
from users.factories import UserFactory


class PostTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = self.refresh_token.access_token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

    def test_post_list(self):
        posts = PostFactory.create_batch(5)
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([post.id for post in posts], [post["id"] for post in response.data])

    def test_post_create(self):
        self.assertEqual(Post.objects.count(), 0)
        data = {
            "title": "My Post",
            "content": "My Content."
        }
        response = self.client.post(reverse('post-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(id=response.data["id"])
        self.assertEqual(post.title, data["title"])
        self.assertEqual(post.author, self.user)

    def test_post_detail(self):
        post = PostFactory()
        response = self.client.get(reverse('post-detail', args=(post.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post.id, response.data['id'])

    def test_post_update(self):
        post = PostFactory()
        data = {
            "title": "New Title"
        }
        self.assertNotEqual(post.id, data["title"])
        response = self.client.patch(reverse('post-detail', args=(post.id,)), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post = Post.objects.get(id=post.id)
        self.assertEqual(post.title, data["title"])

    def test_post_delete(self):
        post = PostFactory()
        response = self.client.delete(reverse('post-detail', args=(post.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_post_like(self):
        post = PostFactory()
        self.assertEqual(post.likes.count(), 0)
        response = self.client.get(reverse('post-like', args=(post.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post = Post.objects.get(id=post.id)
        self.assertEqual(post.likes.count(), 1)
        # verify user can't like twice
        response = self.client.get(reverse('post-like', args=(post.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post = Post.objects.get(id=post.id)
        self.assertEqual(post.likes.count(), 1)

    def test_post_unlike(self):
        post = PostFactory()
        post.likes.add(self.user)
        self.assertEqual(post.likes.count(), 1)
        response = self.client.get(reverse('post-unlike', args=(post.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post = Post.objects.get(id=post.id)
        self.assertEqual(post.likes.count(), 0)
