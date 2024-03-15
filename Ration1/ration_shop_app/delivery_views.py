
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

from django.db.models import Q

class DeliveryOrdersView(TemplateView):
    template_name = 'delivery/delivery_orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location_filter = self.request.GET.get('location')
        if location_filter:
            orders = Cart.objects.filter(
                Q(status='paid', delivery_boy=None) | Q(delivery_boy=self.request.user),
                cust__location=location_filter
            )
        else:
            orders = Cart.objects.filter(
                Q(status='paid', delivery_boy=None) | Q(delivery_boy=self.request.user)
            )
        context['orders'] = orders
        return context

    def post(self, request, *args, **kwargs):
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')
        order = Cart.objects.get(id=order_id)
        if action == 'accept':
            order.delivery_boy = request.user
            order.accepted = True  # Mark the order as accepted
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
        order.accepted = True  # Mark the order as accepted
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


from django.core.mail import send_mail
from django.conf import settings

class DeliveryProcessView(TemplateView):
    template_name = 'delivery/delivery_process.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs['order_id']
        order = Cart.objects.get(id=order_id)
        context['order'] = order
        return context

    def post(self, request, *args, **kwargs):
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')
        order = Cart.objects.get(id=order_id)
        if action == 'accept':
            order.delivery_boy = request.user
            order.accepted = True  # Mark the order as accepted
            order.save()
            # Redirect to the delivery process view
            return redirect('delivery_process', order_id=order.id)
        elif action == 'decline':
            # Delete the order or mark it as declined
            order.delete()
            # Redirect to the delivery orders view
            return redirect('delivery_orders')
        elif action == 'out_for_delivery':
            # Send mail to customer for out for delivery
            customer_email = order.cust.email
            send_mail(
                'Out for Delivery',
                'Your order is out for delivery.',
                settings.EMAIL_HOST_USER,
                [customer_email],
                fail_silently=False,
            )
            messages.success(request, 'Mail sent to customer for Out for Delivery')
        return redirect('delivery_process', order_id=order.id)
