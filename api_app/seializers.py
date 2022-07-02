from pyexpat import model
from rest_framework import serializers
from api_app.models import AdditionalImage, Category, Order


class ImgSerializer(serializers.ModelSerializer):
  class Meta:
    model = AdditionalImage
    fields = ('id','image',)


class CategorySerializer(serializers.ModelSerializer):
  additionalImg = ImgSerializer( read_only=True, many=True)
  class Meta:
    model = Category
    fields = ['id', 'title', 'content', 'image', 'additionalImg']

class OrderSerializer(serializers.ModelSerializer):

  class Meta:
    model = Order
    fields = '__all__'

  def validate(self, data):
    instance = Order(**data)
    instance.clean()
    return data