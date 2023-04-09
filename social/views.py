import requests

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from artsc.consts import Status
from user.models import User

from .models import Post,Category,Friend
from .serializers import PostSerializer,CategorySerializer,FriendSerializer
# Create your views here.

@login_required
def index(request):
    return render(request,"index.html")


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

        r = requests.post("http://34.171.253.227:8080", files=files)
    
    except Exception as e:
        print(e)
        return Response({
            "status":Status.UNSUCCESSFUL,
            "error":e.__str__()
        })
    
    data = r.json()

    print(data)

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

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_network(request):
    friend_requests= Friend.objects.filter(
            (Q(user2=request.user) & Q(accepted = False))
    )

    friends = Friend.objects.filter(
            (Q(user1=request.user) & Q(accepted = True)) |
            (Q(user2=request.user) & Q(accepted=True))
    )

    friend_requests_serialized = FriendSerializer(friend_requests,many = True)
    friends_serialized = FriendSerializer(friends,many = True)

    return Response({
        "status":Status.SUCCESSFUL, 
        "friend_requests_received":friend_requests_serialized.data,
        "friends":friends_serialized.data
    })

    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirm_friend_request(request):
    id = request.data.get("id")

    friend = Friend.objects.get(id=id)
    print(friend)
    friend.accepted = True
    try:
        friend.save()

        return Response({
            "status":Status.SUCCESSFUL,
        })
    except Exception as e:
          return Response({
            "status":Status.UNSUCCESSFUL,
            "error":e.__str__()
        })


