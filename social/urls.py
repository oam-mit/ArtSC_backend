from django.urls import path

from . import views

urlpatterns = [
    path("api/get_categories/",views.get_categories,name="api_get_categories"),
    path("api/upload_post/",views.upload_post,name="api_upload_post"),
    path("api/get_all_posts/",views.get_all_posts,name="api_get_all_posts"),
]