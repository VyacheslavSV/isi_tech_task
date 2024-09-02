from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from app_chat.models import Thread


class ThreadModelTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

    def test_thread_creation(self):
        thread = Thread.objects.create()
        thread.participants.set([self.user1, self.user2])
        thread.save()

        self.assertEqual(Thread.objects.count(), 1)
        self.assertEqual(thread.participants.count(), 2)

    def test_thread_cannot_have_more_than_two_participants(self):
        thread = Thread.objects.create()
        thread.participants.set([self.user1, self.user2])
        thread.save()

        user3 = User.objects.create_user(username='user3', password='password3')
        thread.participants.add(user3)

        with self.assertRaises(ValidationError):
            thread.full_clean()
