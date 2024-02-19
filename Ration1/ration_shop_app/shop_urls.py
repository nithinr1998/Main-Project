from django.urls import path 

from ration_shop_app.shop_views import AddProduct, AddedMemberView, ApproveView, ApprovedmemberView,CustView, Indexview, Member_Approve_Request, Member_Reject_Request, NewCustView, Reject, RejectView, View_Product, View_confirmed_order,HistoryListView

urlpatterns = [

    path('',Indexview.as_view()),
    path('cust_pending_list',NewCustView.as_view(), name='cust_pending_list'),
    path('approve', ApproveView.as_view(),name=''),
    path('reject', RejectView.as_view(),name='reject'),
    path('cust_view',CustView.as_view(),name='cust_viewShop'),
    path('add_product',AddProduct.as_view(),name='add_productShop'),
    path('viewproduct',View_Product.as_view(),name='viewproductShop'),
    path('approvemember',AddedMemberView.as_view(),name='approvemember'),
    path('approvedmember',ApprovedmemberView.as_view(),name='approvedmember'),
    path('aprove_member', Member_Approve_Request.as_view(),name='aprove_member'),
    path('rejectmember',Member_Reject_Request.as_view(),name='rejectmember'),
    path('remove',Reject.as_view(),name='remove'),
    path('history/', HistoryListView.as_view(), name='history'),
    path('order_placed',View_confirmed_order.as_view(),name='order_placed'),
 
 
    
]   


# def urls():
#     return urlpatterns, 'shop','shop'