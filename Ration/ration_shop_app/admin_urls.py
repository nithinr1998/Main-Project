from django.urls import path

from ration_shop_app.admin_views import ApproveView, Indexview,NewShopView, RejectView,AddProduct,AddCard,View_Product,CustView,Reject

urlpatterns = [

    path('',Indexview.as_view()),
    path('pending_shop_list',NewShopView.as_view()),
    path('approve', ApproveView.as_view()),
    path('reject', RejectView.as_view()),
    path('add_card',AddCard.as_view()),
    path('add_product',AddProduct.as_view()),
    path('viewproduct',View_Product.as_view()),
    path('cust_view',CustView.as_view()),
    path('remove', Reject.as_view()),
]


def urls():
    return urlpatterns, 'admin','admin'