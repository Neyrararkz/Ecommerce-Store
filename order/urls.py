from django.urls import path
from . import views

urlpatterns = [
    path('create_order/', views.create_order, name='create_order'),
    path('my_orders/', views.my_orders, name='my_orders')
]
