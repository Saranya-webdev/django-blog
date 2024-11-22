from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status

class PostTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_create_post(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post('/api/posts/', {'title': 'Test Post', 'content': 'This is a test.'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)