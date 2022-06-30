from api_app.models import Order

def check_avalibility (room, arrival_date, departure_date):
  avail_list = []
  order_list = Order.objects.filter(room=room)
  for order in order_list:
    if order.arrival_date > departure_date or order.departure_date < arrival_date:
      avail_list.append(True)
    else:
      avail_list.append(False)
  return all(avail_list)