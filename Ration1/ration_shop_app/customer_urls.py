from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ration_shop_app.customer_views import CartView, Indexview, Payment, UpdateProfile,View_Product,AddMember,ApprovedmemberView,CardOwnerView, View_confirm_order, cancel_order, chpayment, view_cart,ChatbotRedirectView

urlpatterns = [

    path('',Indexview.as_view()),
    path('products_list',View_Product.as_view()),
    path('addmember',AddMember.as_view()),
    path('approvedmember',ApprovedmemberView.as_view()),
    path('cardowner',CardOwnerView.as_view()),
    
    
    path('CartView/<int:id>/', CartView.as_view(), name='cart-view'),
    path('view_cart',view_cart.as_view()),
    path('Payment',Payment.as_view()),
    path('chpayment', chpayment.as_view()),
    path('View_confirm_order',View_confirm_order.as_view()),
    path('cancel_order', cancel_order.as_view()),
    path('updateprofile',UpdateProfile.as_view()),
    path('chatbot/', ChatbotRedirectView.as_view(), name='chatbot_redirect'),
     
    ]


def urls():
    return urlpatterns, 'customer','customer'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)