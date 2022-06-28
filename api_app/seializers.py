from pyexpat import model
from rest_framework import serializers
from api_app.models import AdditionalImage, Category, CustomUser

class AuthUserSerializer(serializers.ModelSerializer):
    # Give user's data
    class Meta:
        model = CustomUser
        fields = ('id','email')



class TrackListingField(serializers.RelatedField):
    def to_representation(self, value):
      return value.image

class ImgSerializer(serializers.ModelSerializer):
    # Give user's data
  
  class Meta:
    model = AdditionalImage
    fields = ('id','image',)


class CategorySerializer(serializers.ModelSerializer):
  additionalImg = ImgSerializer( read_only=True, many=True)
  class Meta:
    model = Category
    fields = ['id', 'title', 'content', 'image', 'additionalImg']

