from django.db import models

from user.models import User

# Create your models here.

class Category(models.Model):
    text = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    default_pic = models.ImageField(upload_to="category_pics",null=True)

    def __str__(self) -> str:
        return self.text
    
    class Meta:
        verbose_name_plural = "Categories"


class Post(models.Model):
    user = models.ForeignKey(to = User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts')
    description =  models.TextField()
    category = models.ForeignKey(to = Category,on_delete=models.SET_NULL,null=True)

    def __str__(self) -> str:
        return f"{self.user.username} {self.category.text}"
    
    

class Friend(models.Model):
    user1 = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name="user1_set")
    user2 = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name="user2_set")
    accepted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user1.email + "--->"+self.user2.email