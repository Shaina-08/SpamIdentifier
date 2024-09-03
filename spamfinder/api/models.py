from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, phone_number, name, password=None, email=None):
        if not phone_number:
            raise ValueError(_('Users must have a phone number'))
        user = self.model(phone_number=phone_number, name=name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, name, password=None, email=None):
        user = self.create_user(phone_number, name, password, email)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
# Models defined for Spam, User, and Contact
class User(AbstractBaseUser):
    name = models.CharField(max_length=100, default='Anonymous')
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=255, blank=True, default='no-reply@example.com')
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Spam(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    is_spam = models.BooleanField(default=True)
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reported_spams',
        default=1 
    )

    def __str__(self):
        return self.phone_number
    
    def reported_by_email(self):
        return self.reported_by.email

class Contact(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contacts'
    )
    phone_number = models.CharField(max_length=15)
    name = models.CharField(max_length=100, default='Unknown')

    def __str__(self):
        return f'{self.name} - {self.phone_number}'
