# urls.py
from django.urls import path
from . import views
from .delivery_views import Indexview, ConfirmDeliveryView, DeliveryCustomerListView,mapview

urlpatterns = [
     path('', Indexview.as_view()),
     path('delivery_order/<int:pk>/', ConfirmDeliveryView.as_view(), name='confirm_delivery'),
     path('customer_list/', DeliveryCustomerListView.as_view(), name='delivery-customer-list'),
     path('map/', mapview.as_view(), name='map'),

     
]
