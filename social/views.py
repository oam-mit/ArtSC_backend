import requests

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from artsc.consts import Status
from user.models import User

from .models import Post,Category,Friend
from .serializers import PostSerializer,CategorySerializer
# Create your views here.

@login_required
def index(request):
    return render(request,"social/index.html")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_posts(request):
    posts = Post.objects.filter()
    serializer = PostSerializer(posts,many=True)
    return Response({
        "status":Status.SUCCESSFUL,
        "posts":serializer.data
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_posts_for_category(request):
    id = request.query_params.get("category_id")
    posts = Post.objects.filter(category__id = id)
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

@api_view(["POST"])
def predict_category(request):
    files = {'file': request.data.get("file").read()}

    try:

        r = requests.post("http://34.27.136.54:8080", files=files)
    
    except Exception as e:
        return Response({
            "status":Status.UNSUCCESSFUL,
            "error":e.__str__()
        })
    
    data = r.json()

    category = Category.objects.get(
        text = data.get("tag")
    )

    serializer = CategorySerializer(
        category
    )

    return Response({
        "status":Status.SUCCESSFUL,
        "category":serializer.data
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_friend_request(request):
    try:
        to = User.objects.get(username=request.data.get("username"))
        friend_requests = Friend.objects.filter(
            user1=request.user,
            user2 = to
        )

        if friend_requests.count() > 0:
            return Response({
                "status":Status.UNSUCCESSFUL,
                "error":"Friend request already sent"
            })
        
        Friend.objects.create(
            user1=request.user,
            user2=to
        )
        return Response({
            "status":Status.SUCCESSFUL
        })
    except Exception as e:
        return Response({
            "status":Status.UNSUCCESSFUL,
            "error":e.__str__()
        })


