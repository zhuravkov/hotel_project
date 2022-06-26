from rest_framework import serializers
from api_app.models import Category, CustomUser

class AuthUserSerializer(serializers.ModelSerializer):
    # Give user's data
    class Meta:
        model = CustomUser
        fields = ('id','email')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'