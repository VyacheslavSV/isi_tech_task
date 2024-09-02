from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from app_chat.models import Thread, Message


class ThreadAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.token = RefreshToken.for_user(self.user1).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_thread(self):
        url = reverse('thread-list')
        data = {'participants': [self.user1.id, self.user2.id]}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Thread.objects.filter(id=response.data['id']).exists())

    def test_get_user_threads(self):
        thread = Thread.objects.create()
        thread.participants.add(self.user1, self.user2)

        url = reverse('thread-user-threads')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class MessageAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.thread = Thread.objects.create()
        self.thread.participants.add(self.user1, self.user2)
        self.token = RefreshToken.for_user(self.user1).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_message(self):
        url = reverse('message-list')
        data = {'text': 'Hello', 'thread': self.thread.id}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Message.objects.filter(id=response.data['id']).exists())

    def test_mark_message_as_read(self):
        message = Message.objects.create(sender=self.user1, text='Hello', thread=self.thread)

        url = reverse('message-mark-as-read', args=[message.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message.refresh_from_db()
        self.assertTrue(message.is_read)
