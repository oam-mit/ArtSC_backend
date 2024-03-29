from django.urls import path

from . import views

app_name = "social"

urlpatterns = [
    path("",views.index,name="index"),
    path("user/<str:username>",views.index,name="user"),
    path("profile",views.index,name="profile"),
    path("new_post",views.index,name="new_post"),
    path("network",views.index,name="network"),
    path("api/get_categories/",views.get_categories,name="api_get_categories"),
    path("api/upload_post/",views.upload_post,name="api_upload_post"),
    path("api/get_all_posts/",views.get_all_posts,name="api_get_all_posts"),
    path("api/predict_category/",views.predict_category,name="api_predict_category"),
    path("api/send_friend_request/",views.send_friend_request,name="api_send_friend_request"),
    path("api/get_posts_for_category/",views.get_posts_for_category,name="api_get_posts_for_category"),
    path("api/get_network/",views.get_network,name="api_get_network"),
    path("api/confirm_friend_request/",views.confirm_friend_request,name="api_confirm_friend_request"),
]