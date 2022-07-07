from pyexpat import model
from rest_framework import serializers
from api_app.models import AdditionalImage, Category, Order, Room


class ImgSerializer(serializers.ModelSerializer):
  class Meta:
    model = AdditionalImage
    fields = ('id','image',)


class CategorySerializer(serializers.ModelSerializer):
  additionalImg = ImgSerializer( read_only=True, many=True)
  class Meta:
    model = Category
    fields = ['id', 'title', 'content', 'image', 'additionalImg']

class RoomSerializer(serializers.ModelSerializer):
  class Meta:
    model = Room
    fields = ("__str__",)
class OrderSerializer(serializers.ModelSerializer):
  order_name = serializers.ReadOnlyField(source='room.__str__')

  days = serializers.ReadOnlyField(source='get_Days')
  price = serializers.ReadOnlyField(source='get_Price')

  class Meta:
    model = Order
    read_only_fields = ('order_name', 'get_Days', 'get_Price')
    fields = '__all__'


  def validate(self, data):
    instance = Order(**data)
    instance.clean()
    return data