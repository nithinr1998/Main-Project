
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
from django.db.models import Count



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

            total_delivery_codes = len(grouped_orders)  # Calculate the total number of orders received

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
        context['total_delivery_codes'] = total_delivery_codes   # Pass the total number of orders received to the context
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


    
    

class DeliveryNotificationView(View):
    template_name = 'Delivery/delivery_notification.html'

    def get(self, request, *args, **kwargs):
        picked_orders = Pay.objects.filter(payment_status='picked').select_related('cust')
        context = {'picked_orders': picked_orders}
        return render(request, self.template_name, context)

class CancelDeliveryView(View):
    def get(self, request, order_id, *args, **kwargs):
        try:
            order = Pay.objects.get(id=order_id)
            order.payment_status = 'paid'
            order.save()
            messages.success(request, 'Delivery canceled successfully.')
        except Pay.DoesNotExist:
            messages.error(request, 'Failed to cancel delivery. Order not found.')
        return redirect('delivery_notification')




from django.core.mail import send_mail
from django.shortcuts import render
from django.views import View
from django.conf import settings
import random
from .models import DeliveryDetail  # Import the model for delivery details
from datetime import date  # Import the date class
import random

class SendOTPView(View):
    def post(self, request):
        # Extract data from the form
        customer_email = request.POST.get('email')
        customer_name = request.POST.get('customer_name')
        address = request.POST.get('address')
        place = request.POST.get('place')
        phone_number = request.POST.get('phone_number')
        items_bought = request.POST.get('items_bought')

        # Generate a random OTP
        otp = str(random.randint(100000, 999999))
        
        # Send the OTP to the customer's email
        send_mail(
            'Subject: OTP for Delivery Service',
            f'Your OTP for delivery verification is: {otp}',
            settings.EMAIL_HOST_USER,
            [customer_email],
            fail_silently=False,
        )
        
        # Store the OTP and delivery_id in the session for verification
        delivery_detail = DeliveryDetail.objects.create(
            customer_name=customer_name,
            email=customer_email,
            address=address,
            place=place,
            phone_number=phone_number,
            items_bought=items_bought,
            delivery_date=date.today()
        )
        request.session['otp'] = otp
        request.session['delivery_id'] = delivery_detail.pk

        messages.success(request, 'OTP sent successfully.')
        return render(request, 'Delivery/check_otp.html')

class CheckOTPView(View):
    def post(self, request):
        entered_otp = request.POST.get('otp')
        delivery_id = request.session.get('delivery_id')

        # Retrieve the DeliveryDetail instance using the delivery_id
        try:
            delivery_detail = DeliveryDetail.objects.get(pk=delivery_id)
        except DeliveryDetail.DoesNotExist:
            # Handle the case where the DeliveryDetail instance does not exist
            message = 'Delivery detail not found. Please try again.'
            return render(request, 'Delivery/check_otp.html', {'message': message})

        if entered_otp == request.session.get('otp'):
            # OTP is correct, update the delivery_success field and save the instance
            delivery_detail.delivery_success = True
            delivery_detail.save()
            return redirect('delivery_success')
        else:
            # OTP is incorrect, display an error message
            message = 'Invalid OTP. Please try again.'
            return render(request, 'Delivery/check_otp.html', {'message': message})

    
    
    
class DeliverySuccessView(View):
    def get(self, request):
        return render(request, 'Delivery/delivery_success.html') 
    
    
    
from django.views.generic import ListView
from .models import DeliveryDetail

class DeliveryHistoryListView(ListView):
    model = DeliveryDetail
    template_name = 'Delivery/delivery_history.html'
    context_object_name = 'delivery_details'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        delivered_orders_count = DeliveryDetail.objects.filter(delivery_success=True).count()
        context['delivered_orders_count'] = delivered_orders_count
        return context