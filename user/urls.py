from django.urls import path

from . import views


app_name = "user"

urlpatterns = [
    path("",views.login_user,name="login"),
    path("register",views.register,name="register_user"),
    path("logout",views.logout_user,name="logout"),
    #APIs
    path("user/api/register/",views.register_user,name="api_user_register_api"),
    path("user/api/login/",views.Login.as_view(),name="api_user_login"),
    path("user/api/get_user_data/",views.get_user_data,name="api_get_user_data"),
    path("user/pi/change_profile_picture/",views.change_profile_picture,name="api_change_profile_picture"),
]