import requests

from django.shortcuts import render

from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from artsc.consts import Status

from .models import Post,Category
from .serializers import PostSerializer,CategorySerializer
# Create your views here.

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_posts(request):
    posts = Post.objects.filter()
    serializer = PostSerializer(posts,many=True)
    return Response({
        "status":Status.SUCCESSFUL,
        "posts":serializer.data
    })



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_post(request):
    try:
        category = Category.objects.get(id = request.data.get("category_id"))
        post = Post.objects.create(
            user = request.user,
            image = request.data.get("image"),
            description = request.data.get("description"),
            category = category
        )

        files = {'file': open(post.image.path,'rb')}

        r = requests.post("http://172.20.10.2:8000", files=files)

        print(r.json())

        return Response({
            "successful":Status.SUCCESSFUL
        })
    except Exception as e:
        return Response({
            "status":Status.UNSUCCESSFUL,
            "error":e.__str__()
        })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_categories(request):
    categories = Category.objects.filter()

    serializer = CategorySerializer(categories,many = True)

    return Response({
        "status":Status.SUCCESSFUL,
        "categories":serializer.data
    })




