from django.shortcuts import render
from django.db.models import Q

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
        user = User.objects.get(username = request.data.get("username"))
        serializer = UserSerializer(user)
        friend = Friend.objects.filter(Q(user1=user))
        return Response({
            "status":Status.SUCCESSFUL,
            "user":serializer.data
        })
    
    except Exception as e:
        return Response({
            "status":Status.UNSUCCESSFUL,
            "error":e.__str__()
        })

 