from rest_framework.serializers import ModelSerializer, StringRelatedField

from .models import Friend, Post, Category

from user.serializers import GetUserSerializer




class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['text','display_name','id','default_pic']


class PostSerializer(ModelSerializer):

    username = StringRelatedField(source="user.username")
    category = CategorySerializer()
    class Meta:
        model = Post
        fields = ['id','image', 'description', 'username', 'category']


class FriendSerializer(ModelSerializer):
    user1 = GetUserSerializer()
    user2 = GetUserSerializer()

    class Meta:
        model = Friend
        fields = ["id","user1","user2","accepted"]
