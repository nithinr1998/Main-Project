
from urllib import request
from django.views import View
from django.shortcuts import render
from django.views.generic import TemplateView
from ration_shop_app.models import Cart,Pay,Customer
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from collections import defaultdict
from django.core.exceptions import ObjectDoesNotExist



class Indexview(TemplateView):
    template_name = 'Delivery/index.html'
    
class mapview(TemplateView):
    template_name = 'Delivery/map.html'    
class DeliveryOrdersView(TemplateView):
    template_name = 'Delivery/delivery_orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Pay.objects.filter(payment_status='paid')

        grouped_orders = defaultdict(list)
        for order in orders:
            grouped_orders[order.cust.id].append(order)
        
        for customer_id, customer_orders in grouped_orders.items():
            total_amount = sum(order.total_amount for order in customer_orders)
            grouped_orders[customer_id] = {
                'customer': customer_orders[0].cust,
                'delivery_code': f'DEL{customer_orders[0].id}',  # Generate a unique delivery code
                'delivery_date': customer_orders[0].payment_date,  # Use the payment_date field
                'total_amount': total_amount,
                'payment_status': customer_orders[0].payment_status,
            }
        
        context['grouped_orders'] = grouped_orders.values()
        return context


class ViewOrderDetailsView(TemplateView):
    template_name = 'Delivery/order_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            customer_id = self.kwargs['customer_id']
            customer_orders = Pay.objects.filter(cust_id=customer_id, payment_status='paid')
            context['customer'] = customer_orders[0].cust
            context['items'] = customer_orders
        except ObjectDoesNotExist:
            messages.error(request, 'The specified order does not exist.')
            return redirect('delivery_orders')
        return context

class MarkAsPickedView(View):
    def post(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        try:
            orders = Pay.objects.filter(cust_id=customer_id, payment_status='paid')
            for order in orders:
                order.payment_status = 'picked'
                order.save()
            messages.success(request, 'Orders marked as picked successfully.')
        except ObjectDoesNotExist:
            messages.error(request, 'Failed to mark orders as picked.')
        return redirect('delivery_orders')

from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.conf import settings
import json

class PickedOrdersView(TemplateView):
    template_name = 'Delivery/picked_orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        picked_orders = Pay.objects.filter(payment_status='picked')

        grouped_orders = defaultdict(list)
        for order in picked_orders:
            grouped_orders[order.cust.id].append(order)
        
        for customer_id, customer_orders in grouped_orders.items():
            total_amount = sum(order.total_amount for order in customer_orders)
            customer = customer_orders[0].cust
            grouped_orders[customer_id] = {
                'order_code': f'ORD{customer_orders[0].id}',  # Assuming order code format
                'customer_name': customer.user.first_name,
                'customer_email': customer.user.email,  # Include the customer's email
                'order_received_date': customer_orders[0].payment_date,
            }
        
        context['picked_orders'] = grouped_orders.values()
        return context

class SendEmailView(TemplateView):
    template_name = 'Delivery/picked_orders.html'

    def post(self, request, *args, **kwargs):
        data = request.POST
        estimated_delivery_date = data.get('estimated_delivery_date')
        customer_email = data.get('customer_email')
        message = ''

        delivery_rules = [
            'Estimated delivery date is not final and may change.',
            'Delivery times are between 9:00 AM and 6:00 PM.',
            'A OTP may be required upon delivery.',
            'Delivery may be delayed due to unforeseen circumstances (e.g., weather conditions, traffic).',
        ]

        try:
            send_mail(
                'Your order is dispatched',
                f'Your order is dispatched with estimated delivery date: {estimated_delivery_date}\n\nDelivery Rules:\n{", ".join(delivery_rules)}',
                settings.EMAIL_HOST_USER,
                [customer_email],
                fail_silently=False,
            )
            message = 'Email sent successfully'
        except Exception as e:
            message = str(e)

        return render(request, self.template_name, {'message': message})