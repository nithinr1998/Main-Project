from django.urls import path
from . import admin_views
from ration_shop_app.admin_views import ApproveView, Indexview,NewShopView, RejectView,AddProduct,AddCard,View_Product,CustView,Reject,ApprovedShopListView,AddDeliveryBoy,DeliveryBoyHistoryView

urlpatterns = [
    
    path('',Indexview.as_view()),
    path('pending_shop_list',NewShopView.as_view(), name='pending_shop_list'),
    path('approve', ApproveView.as_view(), name='approve'),
    path('reject', RejectView.as_view(), name='reject'),
    path('add_card', AddCard.as_view(), name='add_card'),
    path('add_product',AddProduct.as_view(), name='add_product'),
    path('viewproduct',View_Product.as_view(), name='viewproduct'),
    path('cust_view',CustView.as_view(), name='cust_view'),
    path('remove', Reject.as_view(), name='remove'),
    path('approvedshop', ApprovedShopListView.as_view(), name='approvedshop'),
    path('add_delivery_boy/', AddDeliveryBoy.as_view(), name='add_delivery_boy'),
    path('delivery_boys_history/', DeliveryBoyHistoryView.as_view(), name='delivery_boys_history'),
]

    


#def urls():
#    return urlpatterns, 'admin','admin'