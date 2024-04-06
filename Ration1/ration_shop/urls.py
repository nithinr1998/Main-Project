"""
URL configuration for ration_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from django.contrib.auth import views as auth_views

from ration_shop_app.views import IndexView,loginview,Customer_RegView,Shop_RegView,TimeView,blogview,contactview
from ration_shop_app import admin_urls, customer_urls, shop_urls

urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('admin/', admin_urls.urls()),
    path('customer/',customer_urls.urls()),
    path('shop/',include('ration_shop_app.shop_urls')),
    path('admin/',include('ration_shop_app.admin_urls')),
    path('Delivery/',include('ration_shop_app.delivery_urls')),
    path('',IndexView.as_view()),
    path('time',TimeView.as_view()),
   
    path('customerreg',Customer_RegView.as_view(), name='customerreg'),
    path('shopreg',Shop_RegView.as_view(), name='shopreg'),
    path('blog',blogview.as_view(), name='blog'),
    path('login/',loginview.as_view(), name='login'),
    path('contact',contactview.as_view(), name='contact'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset_form'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    
]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)