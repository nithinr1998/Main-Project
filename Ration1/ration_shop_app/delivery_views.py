
from django.views import View
from django.shortcuts import render
from django.views.generic import TemplateView
from ration_shop_app.models import Cart,User,Customer



class Indexview(TemplateView):
    template_name = 'Delivery/index.html'
    

class DeliveryOrderHistoryView(TemplateView):
    template_name = 'Delivery/delivery_order_history.html'

    def get_context_data(self, **kwargs):
        # Fetch orders for the delivery man based on customer ID
        delivered_orders = Cart.objects.filter(cust_id=self.request.user.id, payment='paid')

        context = {
            'delivered_orders': delivered_orders,
        }
        return context
    
class DeliveryCustomerListView(TemplateView):
    template_name = 'Delivery/delivery_customer_list.html'

    def get_context_data(self, **kwargs):
        customers = Customer.objects.all()  # Fetch all customers
        context = {
            'customers': customers,
        }
        return context