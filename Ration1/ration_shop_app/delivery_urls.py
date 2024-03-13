# urls.py
from django.urls import path
from . import views
from .delivery_views import Indexview, DeliveryOrdersView, DeliveryCustomerListView,mapview,AcceptOrderView,RejectOrderView

urlpatterns = [
     path('', Indexview.as_view()),
     path('delivery_orders/', DeliveryOrdersView.as_view(), name='delivery_orders'),
     path('accept_order/<int:id>/', AcceptOrderView.as_view(), name='accept_order'),
     path('reject_order/<int:id>/', RejectOrderView.as_view(), name='reject_order'),
     path('customer_list/', DeliveryCustomerListView.as_view(), name='delivery-customer-list'),
     path('map/', mapview.as_view(), name='map'),

     
]
