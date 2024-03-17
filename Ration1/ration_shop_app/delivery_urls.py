# urls.py
from django.urls import path
from . import views
from .delivery_views import Indexview, DeliveryOrdersView, mapview, ViewOrderDetailsView,MarkAsPickedView,PickedOrdersView,SendEmailView

urlpatterns = [
    path('', Indexview.as_view()),
    path('delivery-orders/', DeliveryOrdersView.as_view(), name='delivery_orders'),
    path('view-order-details/<int:customer_id>/', ViewOrderDetailsView.as_view(), name='view_details'),
    path('mark-as-picked/<int:customer_id>/', MarkAsPickedView.as_view(), name='mark_as_picked'),
    path('picked-orders/', PickedOrdersView.as_view(), name='picked_orders'),
    path('map/', mapview.as_view(), name='map'),
    path('send-email/', SendEmailView.as_view(), name='send_email'),
    
    
]
