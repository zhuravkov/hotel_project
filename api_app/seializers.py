from pyexpat import model
from rest_framework import serializers
from api_app.models import AdditionalImage, Category, Order, Room


class ImgSerializer(serializers.ModelSerializer):
  class Meta:
    model = AdditionalImage
    fields = ('id','image',)


class CategorySerializer(serializers.ModelSerializer):
  additionalImg = ImgSerializer( read_only=True, many=True)
  # photo_url = serializers.SerializerMethodField()

  class Meta:
    model = Category
    fields = ['id', 'title', 'content', 'image', 'category_slug', 'additionalImg', 'price']

  # def get_photo_url(self, obj):
  #     request = self.context.get('request')
  #     photo_url = obj.image
  #     print(photo_url)
  #     return request.build_absolute_uri(photo_url)



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