# urls.py
from django.urls import path
from . import views
from .delivery_views import Indexview, DeliveryOrdersView, DeliveryCustomerListView, mapview, AcceptOrderView,DeliveryProcessView

urlpatterns = [
    path('', Indexview.as_view()),
    
    path('delivery_orders/', DeliveryOrdersView.as_view(), name='delivery_orders'),
    path('accept_order/<int:id>/', AcceptOrderView.as_view(), name='accept_order'),
    path('delivery_process/<int:order_id>/', DeliveryProcessView.as_view(), name='delivery_process'),
    path('customer_list/', DeliveryCustomerListView.as_view(), name='delivery-customer-list'),
    path('map/', mapview.as_view(), name='map'),
]
