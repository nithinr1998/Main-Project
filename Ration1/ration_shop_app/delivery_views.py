
from django.views import View
from django.shortcuts import render
from django.views.generic import TemplateView
from ration_shop_app.models import Cart,User,Customer
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages



class Indexview(TemplateView):
    template_name = 'Delivery/index.html'
    
class mapview(TemplateView):
    template_name = 'Delivery/map.html'    

from django.views.generic import DetailView
from django.shortcuts import redirect
from .models import DeliveryOrder

class ConfirmDeliveryView(DetailView):
    model = DeliveryOrder
    template_name = 'delivery/delivery_order_history.html'
    context_object_name = 'order'

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        action = request.POST.get('action')
        if action == 'accept':
            order.status = 'accepted'
        elif action == 'reject':
            order.status = 'rejected'
        order.save()
        return redirect('delivery_dashboard')  # Redirect to delivery dashboard or another page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = self.request.POST.get('action')
        return context

    
class DeliveryCustomerListView(TemplateView):
    template_name = 'Delivery/delivery_customer_list.html'

    def get_context_data(self, **kwargs):
        customers = Customer.objects.all()  # Fetch all customers
        context = {
            'customers': customers,
        }
        return context


