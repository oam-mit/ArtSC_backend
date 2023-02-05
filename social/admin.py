from django.contrib import admin

from .models import Post,Category,Friend
# Register your models here.


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Friend)