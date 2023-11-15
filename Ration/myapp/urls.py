from django. urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [ 
    path('',views.home,name='myhome'),
    path('contact/',views.contact,name="contact"),
    path('blog/',views.blog,name="blog"),
    path('ration/',views.ration,name="ration"),
    path('customerbase/',views.customerbase,name="customerbase"),
    path('shopowner/',views.shopowner,name="shopowner"),
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
    path('purchese/',views.purchese,name="purchese"),
    path('history/',views.history,name="history"),
    path('shophistory/',views.shophistory,name="shophistory"),
    path('shoptiming/',views.shoptiming,name="shoptiming"),
    path('custtiming/',views.custtiming,name="custtiming"),
    path('customer/',views.customer,name="customer"),
    path('customerlist/', views.customer_list, name='customer_list'),
    path('shopownerlist/', views.shopowner_list, name='shopowner_list'),
    path('memberlist/', views.member_list, name='member_list'),
    path('viewmember_list/', views.viewmember_list, name='viewmember_list'),
    path('admin_stock/', views.admin_stock, name='admin_stock'),
    path('admin_item/', views.admin_item, name='admin_item'),
    path('add_carditem/',views.add_carditem, name='add_carditem'),
    path('admin_view_carditem/',views.admin_view_carditem, name='admin_view_carditem'),
    path('view_item/', views.view_item, name='view_item'),
    path('shopcarditem/', views.shopcarditem, name='shopcarditem'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('admincustomer_list',views.admincustomer_list, name='admincustomer_list'),
    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
   
    
    
      
      
    
]
