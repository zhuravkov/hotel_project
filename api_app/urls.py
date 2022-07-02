from django.urls import path

from api_app.views import OrderView, categories_view



urlpatterns = [
    path('categories', categories_view),
    path('order', OrderView.as_view()),

]
