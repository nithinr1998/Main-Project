# urls.py
from django.urls import path
from . import views
from .delivery_views import Indexview, DeliveryOrderHistoryView, DeliveryCustomerListView

urlpatterns = [
     path('', Indexview.as_view()),
     path('order_history/', DeliveryOrderHistoryView.as_view(), name='delivery-order-history'),
     path('customer_list/', DeliveryCustomerListView.as_view(), name='delivery-customer-list'),
     
]
