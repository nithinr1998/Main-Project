from django.urls import path

from ration_shop_app.shop_views import AddProduct, AddedMemberView, ApproveView, ApprovedmemberView,CustView, Indexview, Member_Approve_Request, Member_Reject_Request, NewCustView, Reject, RejectView, View_Product, View_confirmed_order

urlpatterns = [

    path('',Indexview.as_view()),
    path('cust_pending_list',NewCustView.as_view()),
    path('approve', ApproveView.as_view()),
    path('reject', RejectView.as_view()),
    path('cust_view',CustView.as_view()),
    path('add_product',AddProduct.as_view()),
    path('viewproduct',View_Product.as_view()),
    path('approvemember',AddedMemberView.as_view()),
    path('approvedmember',ApprovedmemberView.as_view()),
    path('aprove_member', Member_Approve_Request.as_view()),
    path('rejectmember',Member_Reject_Request.as_view()),
    path('remove',Reject.as_view()),
    path('order_placed',View_confirmed_order.as_view())
]   


def urls():
    return urlpatterns, 'shop','shop'