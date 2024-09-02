from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker

from app_chat.models import Thread, Message


class Command(BaseCommand):
    help = 'Populate the database with fake data.'

    def handle(self, *args, **kwargs):
        fake = Faker()
        users = [User.objects.create(username=fake.user_name(), password='password123') for _ in range(10)]

        # Create threads with random participants
        for _ in range(5):
            participants = fake.random_elements(elements=users, length=2, unique=True)
            thread = Thread.objects.create()
            thread.participants.set(participants)
            thread.save()

            # Create messages for each thread
            for _ in range(10):
                Message.objects.create(
                    sender=fake.random_element(elements=users),
                    text=fake.text(),
                    thread=thread
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with fake data.'))
