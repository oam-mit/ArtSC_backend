from .models import User

from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["username","email","first_name","last_name","password"]

    def save(self):
        user = User(
            username = self.validated_data.get("username"),
            email = self.validated_data.get("email"),
            first_name = self.validated_data.get("first_name"),
            last_name = self.validated_data.get("last_name")
        )

        user.set_password(self.validated_data.get("password"))

        user.save()
        return user