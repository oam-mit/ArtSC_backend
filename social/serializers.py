from rest_framework.serializers import ModelSerializer, StringRelatedField

from .models import Post, Category





class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['text','display_name','id']


class PostSerializer(ModelSerializer):

    username = StringRelatedField(source="user.username")
    category = CategorySerializer()
    class Meta:
        model = Post
        fields = ['image', 'description', 'username', 'category']