
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

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from ration_shop_app.models import Cart

class DeliveryOrdersView(TemplateView):
    template_name = 'delivery/delivery_orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location_filter = self.request.GET.get('location')
        if location_filter:
            orders = Cart.objects.filter(status='paid', delivery_boy=None, cust__location=location_filter)
        else:
            orders = Cart.objects.filter(status='paid', delivery_boy=None)
        context['orders'] = orders
        return context

    def post(self, request, *args, **kwargs):
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')
        order = Cart.objects.get(id=order_id)
        if action == 'accept':
            order.delivery_boy = request.user
            order.save()
            # Redirect to the delivery process view
            return redirect('delivery_process', order_id=order.id)
        elif action == 'reject':
            order.delete()
        return redirect('delivery_orders')

    
from django.shortcuts import redirect
from django.views import View

class AcceptOrderView(View):
    def post(self, request, *args, **kwargs):
        order_id = request.POST.get('order_id')
        order = Cart.objects.get(id=order_id)
        order.delivery_boy = request.user
        order.save()
        # Redirect to the delivery process view
        return redirect('delivery_process', order_id=order_id)



    
class DeliveryCustomerListView(TemplateView):
    template_name = 'Delivery/delivery_customer_list.html'

    def get_context_data(self, **kwargs):
        customers = Customer.objects.all()  # Fetch all customers
        context = {
            'customers': customers,
        }
        return context


from django.core.exceptions import ObjectDoesNotExist

class DeliveryProcessView(TemplateView):
    template_name = 'delivery/delivery_process.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            order_id = self.kwargs['order_id']
            order = Cart.objects.get(id=order_id)
            context['order'] = order
        except ObjectDoesNotExist:
            # Handle the case where the Cart object does not exist
            return redirect('delivery_orders')
        return context