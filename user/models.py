from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from  django.dispatch import receiver

from rest_framework.authtoken.models import Token

# Create your models here.
class User(AbstractUser):
    profile_photo = models.ImageField(upload_to='profile_pics',default='default.jpeg')
    def __str__(self) -> str:
        return self.email
    


@receiver(post_save,sender=User)
def create_token(sender,instance=None,created=False,**kwargs):
    print("Called")
    if created:
        Token.objects.create(user=instance)