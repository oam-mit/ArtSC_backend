from django.shortcuts import render,redirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import authenticate,logout,login


from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from artsc.consts import Status
from social.models import Friend

from .models import User
from .serializers import UserSerializer
# Create your views here.

def login_user(request):
    if request.method =="POST":
        user = authenticate(username = request.POST.get('username'),password = request.POST.get("password"))

        if user is not None:
            login(request,user)
            return redirect(reverse("social:index"))
        else:
            return render(request,"user/login.html")
    return render(request,"user/login.html")


def register(request):
    if request.method == "POST":
        try:
            user = User(
            username = request.POST.get("username"),
            email = request.POST.get("email"),
            first_name = request.POST.get("first_name"),
            last_name = request.POST.get("last_name")
        )
            user.set_password(request.POST.get("password"))

            user.save()

            return redirect(reverse("user:login"))
            
        except Exception as e:
            return render(request,"user/register.html")

        

        user.save()

    return render(request,"user/register.html")


def logout_user(request):
    logout(request)
    return redirect(reverse("user:login"))


@api_view(["POST"])
def register_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        try:
            user =serializer.save()
            
            return Response({
                "status":"successful",
                "username":user.username,
                "first_name":user.first_name,
                "last_name":user.last_name,
                "email":user.email,
                "profile_photo":user.profile_photo.url,
                "token":user.auth_token.key
            })
        except Exception as e:
            return Response({
                "status":Status.UNSUCCESSFUL,
                "error":e.__str__()
            })
    else:
        return Response({
            "status":Status.UNSUCCESSFUL,
            "error":"username already exists"
        })


class Login(ObtainAuthToken):


    def post(self, request, *args, **kwargs):
        context={}
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=False):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            context['status']=Status.SUCCESSFUL
            context['token']=token.key
            context['email']=user.email
            context['first_name']=user.first_name
            context['last_name']=user.last_name
            context["profile_photo"] = user.profile_photo.url
            context["username"] = user.username

        else:
            context['status']=Status.UNSUCCESSFUL
            context["error"] = "Invalid Credentials"
        return Response(context)
    


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_data(request):
    try:
        user = User.objects.get(username = request.query_params.get("username"))
        serializer = UserSerializer(user)
        friend = Friend.objects.filter(
            (Q(user1=user) & Q(user2=request.user)) |
            (Q(user1=request.user) & Q(user2=user))
        )
        if friend.count() > 0:
            if friend.first().accepted:
                friend_status = "FRIEND"
            else:
                friend_status = "SENT"
        else:
            friend_status = "NOT A FRIEND"
        return Response({
            "status":Status.SUCCESSFUL,
            "user":serializer.data,
            "friend": friend_status
        })
    
    except Exception as e:
        return Response({
            "status":Status.UNSUCCESSFUL,
            "error":e.__str__()
        })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_profile_picture(request):
    try:
        request.user.profile_photo = request.data.get("image")
        request.user.save()
    except Exception as e:
        return Response({
            "status":Status.UNSUCCESSFUL,
            "error": e.__str__()
        })

    return Response({
        "status":Status.SUCCESSFUL,
        "profile_photo":request.user.profile_photo.url
    })