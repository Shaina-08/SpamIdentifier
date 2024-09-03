from django.core.management.base import BaseCommand
from api.models import User, Contact

class Command(BaseCommand):
    help = 'Add a contact to the database'

    def handle(self, *args, **kwargs):
     
        user = User.objects.first()  
        phone_number = '7876726829'
        name = 'Test Contact'
        
        if user:
            Contact.objects.create(user=user, phone_number=phone_number, name=name)
            self.stdout.write(self.style.SUCCESS(f'Successfully added contact with phone number {phone_number}'))
        else:
            self.stdout.write(self.style.ERROR('No user found to associate with the contact'))
