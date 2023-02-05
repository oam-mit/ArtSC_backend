from django.urls import path

from . import views

urlpatterns = [
    path("api/register/",views.register_user,name="api_user_register_api"),
    path("api/login/",views.Login.as_view(),name="api_user_login"),
    path("api/get_user_data/",views.get_user_data,name="api_get_user_data"),
    path("api/change_profile_picture/",views.change_profile_picture,name="api_change_profile_picture"),
]