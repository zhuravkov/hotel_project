import datetime as dt

from rest_framework import status
from rest_framework.response import Response

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from api_app.booking_functions.availability import check_avalibility
from api_app.booking_functions.count_price import count_price

from api_app.models import Category, Order, Room, SeasonRatio
from api_app.seializers import CategorySerializer, OrderSerializer

from rest_framework.generics import CreateAPIView, ListAPIView


def index(request):
    return render (request, 'index.html', {})


@api_view(['GET'])
def categories_view (request):
  try:
    categories = Category.objects.all()
    serializer_context = {
    'request': None,
}
    serializer = CategorySerializer(categories, many=True, context=serializer_context)
    return JsonResponse({'data':serializer.data, 'resultCode': 0, 'messages': 'Success'})

  except Category.DoesNotExist:
    return JsonResponse({ 'data':{}, 'resultCode': 1, 'messages':'ERROR'})

# Создать заказ
class OrderView(CreateAPIView, ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        # Всё делаю здесь т.к не жду номер комнаты от фронта а назначаю 
        # его здесь перед 1 передачей в сериализатор
        # если делать в def perform_create(self, serializer): будет ошибка
        # что room не может отсутствовать
        # 1 переводим даты в нужный формат
        arrival_date_req=dt.datetime.strptime(self.request.data.get('arrival_date'), "%Y-%m-%d").date()
        departure_date_req=dt.datetime.strptime(self.request.data.get('departure_date'), "%Y-%m-%d").date()
        if departure_date_req<arrival_date_req:
          return JsonResponse({'data': {}, 'resultCode': 1, 'messages': 'WRONG DATES'})
        # Выбираю комнаты заданной категории
        rooms_cat = Room.objects.filter(category__id = self.request.data.get('category'))
        # Создаю множество уникальных номеров
        free_rooms_set = set()  
        # Итерирую комнаты и проверяю наличие в них заказов на указанные даты
        for room in rooms_cat:
          if check_avalibility(room,arrival_date_req, departure_date_req):
            # если заказов нет комната добавляется в множество
            free_rooms_set.add(room)
        # множество в список
        free_rooms = list(free_rooms_set)
        if len(free_rooms)>0 :
          # если в списке есть номера то первый в списке записываем и идем дальше
          booking_room = free_rooms[0]
          request.data['room'] = booking_room.pk
        else:
          # если список пустой, сразу отдаю ответ не передавая данные в сериализатор
          return JsonResponse({ 'data':{}, 'resultCode': 1, 'messages':'Выберите другую категорию или даты'})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # после сериализации отдаем ответ
        return JsonResponse({ 'data':serializer.data, 'resultCode': 0, 'messages':'Booking is success'})
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

@api_view(['GET'])
def calculate_view(request):
  if request.method == 'GET':
    try:
      category_req = request.GET['category']
      arrival_date_req = dt.datetime.strptime(
          request.GET['arrival_date'], "%Y-%m-%d").date()
      departure_date_req = dt.datetime.strptime(
          request.GET['departure_date'], "%Y-%m-%d").date()

      if departure_date_req<arrival_date_req:
        return JsonResponse({'data': {}, 'resultCode': 1, 'messages': 'WRONG DATES'})

      current_category = Category.objects.get(id=category_req)
      ratio = SeasonRatio.objects.all()

      current_price = count_price(
          current_category, arrival_date_req, departure_date_req, ratio)
          
      days = (departure_date_req - arrival_date_req).days
      # REMAKE DUBLICATE ORDER VIEW
      rooms_cat = Room.objects.filter(category__pk=current_category.pk)

      free_rooms_set = set()
      for room in rooms_cat:
            if check_avalibility(room, arrival_date_req, departure_date_req):
              free_rooms_set.add(room)
      free_rooms = list(free_rooms_set)

      return JsonResponse({ 'data':{'price':current_price, 'days':days, 'avalibility':len(free_rooms)},
                             'resultCode': 0, 'messages':''})
    except:
      return JsonResponse({'data': {}, 'resultCode': 1, 'messages': 'ERROR'})



