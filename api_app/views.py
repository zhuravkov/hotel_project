import datetime as dt

from rest_framework import status
from rest_framework.response import Response

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view

from api_app.models import Category, Order, Room, check_avalibility
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
        # Выбираю комнаты заданной категории
        rooms_cat = Room.objects.filter(category__pk = self.request.data.get('category'))
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
          print('Select anothe category or dates')
          return JsonResponse({ 'data':{}, 'resultCode': 1, 'messages':'Select another category or dates'})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print(serializer.data)
        # после сериализации отдаем ответ
        return JsonResponse({ 'data':serializer.data, 'resultCode': 0, 'messages':'Booking is success'})
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

