
from django.urls import path
from arkapp import views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

urlpatterns = [
      path('',views.index,name='index'),
      path('collections/',views.collections,name='collections'),
      path('login',views.loginn,name='loginpage'),
      path('Register',views.register,name='Registrationpage'),
      path('logout',views.logout,name="logout"),
      path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
      path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
      path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
      path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
      path('blog/', views.blog, name='blog'),
      path('contact/', views.contact, name='contact'),
]
