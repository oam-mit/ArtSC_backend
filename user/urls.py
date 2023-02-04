from django.urls import path

from . import views

urlpatterns = [
    path("api/register/",views.register_user,name="api_user_register_api"),
    path("api/login/",views.Login.as_view(),name="api_user_login"),
]