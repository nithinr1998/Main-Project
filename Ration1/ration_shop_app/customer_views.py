from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import TemplateView

from ration_shop_app.models import Cart, Customer, Member, Product,Card,Product_Item

class Indexview(TemplateView):
    template_name = 'customer/index.html'
    
class View_Product(TemplateView):
   template_name = 'customer/products_list.html'

   def get_context_data(self, **kwargs):
        context = super(View_Product, self).get_context_data(**kwargs)
        cust = Customer.objects.get(user_id=self.request.user.id)
        view_pp = Product.objects.filter(card_id=cust.id)
        context['view_pp'] = view_pp
        im=Product_Item.objects.all()
        context['im'] = im
        return context


    
     
class AddMember(TemplateView):
    template_name = 'customer/addmember.html'
    def get_context_data(self, **kwargs):
        context = super(AddMember, self).get_context_data(**kwargs)
        view_pp = Card.objects.all()
        context['view_pp'] = view_pp
        return context 
    
    def post(self, request, *args, **kwargs):
        cust = Customer.objects.get(user_id=self.request.user.id)
        name = request.POST['name']
        relation = request.POST['relation']
        age = request.POST['age']
        gender = request.POST['gender']
        job = request.POST['job']
        card = request.POST['card']                                    
        reg = Member()
        
        reg.cust_id = cust.id
        reg.name = name
        reg.relation = relation
        reg.age = age
        reg.gender = gender
        reg.job = job
        reg.card_id = card
        reg.status = "added"
        reg.save()
        
        return render(request, 'customer/index.html',{'message': "Member successfully added "})
    
class CardOwnerView(TemplateView):
    template_name = 'customer/cardowner.html'

    def get_context_data(self, **kwargs):
        context = super(CardOwnerView, self).get_context_data(**kwargs)
        id1=self.request.user.id
        
        custom = Customer.objects.filter(user_id=id1)
        # context['users'] = user
        context['custom'] = custom
        return context
    
class ApprovedmemberView(TemplateView):
    template_name = 'customer/approvedmemberlist.html'
    
    def get_context_data(self, **kwargs):
        context = super(ApprovedmemberView, self).get_context_data(**kwargs)
        cust = Customer.objects.get(user_id=self.request.user.id)
        view1 = Member.objects.filter(status='Approved',cust_id=cust.id)
        context['view1'] = view1
        return context
    
from decimal import Decimal

class CartView(TemplateView):
    template_name = 'customer/products_list.html'

    def dispatch(self, request, *args, **kwargs):
        id = kwargs.get('id')

        # Use get_object_or_404 to handle the case where the product with the given 'id' does not exist
        product = get_object_or_404(Product, pk=id)

        ca = Cart()
        re = Customer.objects.get(user_id=self.request.user.id)

        # Handle the case where 'total_quantity' is None
        qty = re.total_quantity
        if qty is None:
            qty = 0

        # Handle the case where 'product.quantity' is None
        product_quantity = product.quantity
        if product_quantity is None:
            product_quantity = 0

        # Convert the quantities to integers
        qty = int(qty)
        product_quantity = int(product_quantity)

        # Update the product quantity
        product.quantity = max(0, product_quantity - qty)

        # Calculate and set the amount in the Cart model
        ca.amount = product.amount
        ca.quantity = product.quantity

        # Save the changes
        product.save()
        ca.payment = 'null'
        ca.product = product
        ca.cust = re
        ca.status = 'cart'
        ca.save()

        return redirect(request.META['HTTP_REFERER'], {'message': "cart"})
    
    

class view_cart(TemplateView):
    template_name = 'customer/cartview.html'

    def get_context_data(self, **kwargs):
        context = super(view_cart, self).get_context_data(**kwargs)
        cust = Customer.objects.get(user_id=self.request.user.id)
        cart_items = Cart.objects.filter(status='cart', cust_id=cust.id)
        total = 0

        for cart_item in cart_items:
            # Assuming each Cart item has a 'quantity' field
            quantity = int(cart_item.quantity) if cart_item.quantity else 0
            amount = int(cart_item.amount) if cart_item.amount else 0

            total += amount * quantity

        context['view_cart'] = cart_items
        context['asz'] = total

        return context
class Payment(TemplateView):
    template_name = 'customer/payment.html'

    def get_context_data(self, **kwargs):
        context = super(Payment, self).get_context_data(**kwargs)
        user = Customer.objects.get(user_id=self.request.user.id)
        ct = Cart.objects.filter(status='cart', cust_id=user.id)

        total = 0
        for i in ct:
            total = total + int(i.amount)

        context['view'] = ct
        context['asz'] = total

        return context

class chpayment(TemplateView):
    def dispatch(self,request,*args,**kwargs):

        user = Customer.objects.get(user_id=self.request.user.id)


        ch = Cart.objects.filter(cust_id=user.id,status='cart')


        print(ch)
        for i in ch:
            i.payment = 'paid'
            i.status = 'paid'
            i.save()
        return render(request,'customer/index.html',{'message':" payment Success"})
    
    
from django.db.models import Sum    
class View_confirm_order(TemplateView):
    template_name = 'customer/view_order.html'

    def get_context_data(self, **kwargs):
        user = Customer.objects.get(user_id=self.request.user.id)

        pro = Cart.objects.filter(cust_id=user.id, payment='paid')
        
        # Calculate total amount paid
        total_amount_paid = pro.aggregate(total_amount=Sum('amount'))['total_amount']

        context = {
            'pro': pro,
            'total_amount_paid': total_amount_paid,
        }
        return context
    
class cancel_order(TemplateView):

    def dispatch(self,request,*args,**kwargs):
        id = request.GET['id']
        id1=request.GET['id1']
        order=Cart.objects.get(id=id)

        order.delete()


        return redirect(request.META['HTTP_REFERER'],{'message':"cart"})
    
class UpdateProfile(TemplateView):
    template_name = 'customer/updateprofile.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateProfile, self).get_context_data(**kwargs)
        usid = self.request.user.id

        view_cust = Customer.objects.get(user_id=usid)
        print(view_cust)

        context['view_cust'] = view_cust
        return context
    
    def post(self, request, *args, **kwargs):

        if request.POST['profile'] == "pass":
            id = request.POST['id']
            password = request.POST['password']
            us = User.objects.get(pk=id)

            us.set_password(password)

            us.save()
        else:
            
            name =request.POST['name']
            id = request.POST['id']
            card_number =request.POST['card_number']
            email = request.POST['email']
            contact = request.POST['contact']
            address = request.POST['address']
            location = request.POST['location']
            
            reg = Customer.objects.get(user=id)

            reg.card_number =card_number
            reg.contact = contact   
            reg.address = address 
            reg.location = location 
            reg.save()
            us = User.objects.get(pk=id)
            us.username = email
            us.email = email
            us.first_name = name
            us.save()

        messages = "Update Successful."
        return render(request, 'customer/index.html', {'messages': "Update Successful"})
    
    
from django.views import View
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

class ChatbotRedirectView(View):
    @never_cache
    @login_required(login_url='accounts:login')
    def post(self, request):
        message = request.POST.get('message')

        # Check if the message is a greeting
        if message.lower() in ['hello', 'hai', 'hi', 'hola']:
            response_message = "How can I help you?"
            return JsonResponse({'response_message': response_message})

        # Check if the message contains the word 'packages' or 'package'
        if 'packages' in message.lower() or 'package' in message.lower():
            # If 'packages' is found in the message, construct the response with a link to view packages
            view_packages_link = reverse('matdest:view_packages')
            booked_packages_link = reverse('matdest:my_packages')

            response_message = "Here are some matching links:<br>"
            response_message += f"<a href='{view_packages_link}'>View Packages</a><br>"
            response_message += f"<a href='{booked_packages_link}'>Show Booked Packages</a>"
            return JsonResponse({'response_message': response_message})

        # Implement your logic here to determine the redirect URL based on the message
        if message.lower() == 'premium':
            response_message = "Click to get more details of premium: <a href='{}'>Premium</a>".format(reverse('matpayment:view_premium'))
            return JsonResponse({'response_message': response_message})
        
        if message.lower() == 'booking':
            response_message = "Click to get more details of booked packages: <a href='{}'>My Bookings</a>".format(reverse('matdest:my_packages'))
            return JsonResponse({'response_message': response_message})
        
        if 'chat' in message.lower() or 'chats' in message.lower() or 'message' in message.lower():
            response_message = "Click to get mychats: <a href='{}'>Chats</a>".format(reverse('matchat:mychats'))
            return JsonResponse({'response_message': response_message})
        else:
            redirect_url = '/path/to/default/view/'  # Replace with the default URL

        # If the message doesn't match any predefined responses, construct a default response
        default_response = "Sorry, your query didn't match any of our options."
        return JsonResponse({'response_message': default_response})
