from django. urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [ 
    path('',views.home,name='index'),
    path('contact/',views.contact,name="contact"),
    path('about/',views.about,name="about"),
    path('customersignup/',views.customersignup,name="customersignup"),
    path('shopownersignup/',views.shopownersignup,name="shopownersignup"),
    path('signin/',views.signin,name="signin"),
    path('signout/',views.logout_view,name="logout"),
    path('viewc/',views.viewcustomers,name="viewc"),  
    path('addstock/',views.addstock,name="addstock"),
    path('viewstock/',views.viewstock,name="viewstock"),
    path('viewcuststock/',views.viewcuststock,name="viewcuststock"),
    path('addmembers/',views.addmembers,name="addmembers"),
    path('viewmembers/',views.viewmembers,name="viewmembers"),
    path('shophistory/',views.shophistory,name="shophistory"),
    path('shoptiming/',views.shoptiming,name="shoptiming"),
    path('custtiming/',views.custtiming,name="custtiming"),
    path('customerbase/',views.customerbase,name="customerbase"),
    #path('ration/',views.ration,name="ration"),
    path('ration/',views.ration_price,name="ration"),
    path('customerlist/', views.customer_list, name='customer_list'),
    path('customer/', views.customer_base_view, name='customer'),
    path('shopownerlist/', views.shopowner_list, name='shopowner_list'),
    path('memberlist/', views.member_list, name='member_list'),
    path('viewmember_list/', views.viewmember_list, name='viewmember_list'),
    path('admin_stock/', views.admin_stock, name='admin_stock'),
    path('admin_item/', views.admin_item, name='admin_item'),
    path('add_carditem/',views.add_carditem, name='add_carditem'),
    path('admin_view_carditem/',views.admin_view_carditem, name='admin_view_carditem'),
    path('view_item/', views.view_item, name='view_item'),
    path('shopownerbase/', views.shopownerbase, name='shopownerbase'),
    path('shopcarditem/', views.shopcarditem, name='shopcarditem'),
    path('collections/', views.collections, name='collections'),
    path('blog/', views.blog, name='blog'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    
   
    
    
      
      
    
]
