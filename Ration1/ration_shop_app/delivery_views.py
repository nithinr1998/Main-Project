
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


from django.views.generic import TemplateView
from ration_shop_app.models import Cart

class DeliveryOrdersView(TemplateView):
    template_name = 'delivery/delivery_orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Cart.objects.filter(status='paid', delivery_boy=None)
        context['orders'] = orders
        return context

    def post(self, request, *args, **kwargs):
        order_id = kwargs['id']
        action = request.POST.get('action')
        order = Cart.objects.get(id=order_id)
        if action == 'accept':
            order.delivery_boy = request.user
            order.save()
        elif action == 'reject':
            order.delete()
        return redirect('delivery_orders')


    
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from .models import Cart

class AcceptOrderView(View):
    def post(self, request, id):
        order = get_object_or_404(Cart, id=id)
        order.delivery_boy = request.user
        order.save()
        return redirect('delivery_orders')

class RejectOrderView(View):
    def post(self, request, id):
        order = get_object_or_404(Cart, id=id)
        order.delete()
        return redirect('delivery_orders')


    
class DeliveryCustomerListView(TemplateView):
    template_name = 'Delivery/delivery_customer_list.html'

    def get_context_data(self, **kwargs):
        customers = Customer.objects.all()  # Fetch all customers
        context = {
            'customers': customers,
        }
        return context


