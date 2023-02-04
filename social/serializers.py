from rest_framework.serializers import ModelSerializer,StringRelatedField

from .models import Post

class PostSerializer(ModelSerializer):

    username = StringRelatedField(source = "user.username")
    category = StringRelatedField(source = "category.text")

    class Meta:
        model = Post
        fields = ['image','description','username','category']