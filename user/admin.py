from django.contrib import admin

from user.models import User

from django.contrib.auth.admin import UserAdmin

# Register your models here.


class CustomUserAdmin(UserAdmin):
    pass


admin.site.register(User,CustomUserAdmin)