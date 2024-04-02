# urls.py
from django.urls import path
from . import views
from .delivery_views import Indexview, DeliveryOrdersView, mapview, ViewOrderDetailsView,MarkAsPickedView,DeliveryNotificationView,CancelDeliveryView,SendOTPView,CheckOTPView,DeliverySuccessView,DeliveryHistoryListView

urlpatterns = [
    path('', Indexview.as_view()),
    path('delivery-orders/', DeliveryOrdersView.as_view(), name='delivery_orders'),
    path('view-order-details/<int:customer_id>/', ViewOrderDetailsView.as_view(), name='view_details'),
    path('mark-as-picked/<int:customer_id>/', MarkAsPickedView.as_view(), name='mark_as_picked'),
    path('map/', mapview.as_view(), name='map'),
    path('delivery-notification/', DeliveryNotificationView.as_view(), name='delivery_notification'),
    path('cancel-delivery/<int:order_id>/', CancelDeliveryView.as_view(), name='cancel_delivery'),
    path('send_otp/', SendOTPView.as_view(), name='send_otp'),
    path('check_otp/', CheckOTPView.as_view(), name='check_otp'),
    path('delivery_success/', DeliverySuccessView.as_view(), name='delivery_success'),
     path('delivery_history/', DeliveryHistoryListView.as_view(), name='delivery_history'),
]
    

