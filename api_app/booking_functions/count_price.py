import datetime as dt

def count_price(current_category, arrival_date, departure_date, ratio):

    each_day_of_order = []
    delta = departure_date - arrival_date
    # извлекаем каждый день из периода и делаем из них массив
    for i in range(delta.days):
      each_day_of_order.append(arrival_date + dt.timedelta(i))
    all_price_array = []
    # к каждому дню ищем свой коэффициент и добавляем
    #  в массив итоговую стоимость конкретного дня
    for day in each_day_of_order:
      if ratio.exists:
        current_ratio = ratio.filter(
            start_date__lte=day, end_date__gte=day).first().ratio
      else:
        current_ratio = 1
      all_price_array.append(current_ratio*current_category.price)
    # возвращаем сумму за период
    return round(sum(all_price_array))
