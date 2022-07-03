from django.urls import path

from api_app.views import OrderView, calculate_view, categories_view



urlpatterns = [
    path('categories', categories_view),
    path('order', OrderView.as_view()),
    path('calculate', calculate_view),
]
