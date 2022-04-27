from rest_framework import serializers
from api_app.models import CustomUser

class AuthUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id','email')