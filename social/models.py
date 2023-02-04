from django.db import models

from user.models import User

# Create your models here.

class Category(models.Model):
    text = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.text

class Post(models.Model):
    user = models.ForeignKey(to = User,on_delete=models.CASCADE)
    image = models.ImageField()
    description =  models.TextField()
    category = models.ForeignKey(to = Category,on_delete=models.SET_NULL,null=True)

    def __str__(self) -> str:
        return f"{self.user.username} {self.category.text}"
