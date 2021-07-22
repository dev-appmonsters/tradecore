from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


from posts.factories import PostFactory
from users.factories import UserFactory

User = get_user_model()


class UserTest(APITestCase):
    def test_user_signup(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "abc@gmail.com",
            "password": "Ab@123",
            "confirm_password": "Ab@123"
        }
        response = self.client.post(reverse('signup'), data=data, REMOTE_ADDR='54.182.0.19')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.first()
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.ip_address, '54.182.0.19')
        self.assertEqual(user.country_code, 'US')

    def test_get_user_access_token(self):
        password = 'Ab@123'
        user = UserFactory(email='abc@gmail.com', password=make_password(password))
        user.set_password(password)
        response = self.client.post(reverse('token_obtain'), data={"email": user.email, "password": password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # verify access_token
        PostFactory()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(response.data["access"]))
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
