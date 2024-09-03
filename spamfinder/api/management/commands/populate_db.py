from django.core.management.base import BaseCommand
from api.models import User, Spam, Contact
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
      
        for _ in range(10):
            name = fake.name()
            phone_number = fake.phone_number()
            email = fake.email()
            password = 'password123'
            User.objects.create_user(phone_number=phone_number, name=name, email=email, password=password)
        
        users = User.objects.all()
        for _ in range(20):
            phone_number = fake.phone_number()
            reported_by = random.choice(users)
            Spam.objects.create(phone_number=phone_number, is_spam=True, reported_by=reported_by)

      
        users = User.objects.all()
        for user in users:
            for _ in range(5):
                name = fake.name()
                phone_number = fake.phone_number()
                Contact.objects.create(user=user, phone_number=phone_number, name=name)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))
