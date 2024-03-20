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
        card = cust.card  # Assuming Customer model has a 'card' field
        cart_items = Cart.objects.filter(status='cart', cust=cust)
        cart_product_ids = cart_items.values_list('product_id', flat=True)
        view_pp = Product.objects.exclude(id__in=cart_product_ids).filter(card=card)
        context['view_pp'] = view_pp
        im = Product_Item.objects.all()
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
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from .models import Cart, Product, Customer

class CartView(TemplateView):
    template_name = 'customer/products_list.html'

    def dispatch(self, request, *args, **kwargs):
        id = kwargs.get('id')
        product = get_object_or_404(Product, pk=id)
        re = Customer.objects.get(user_id=self.request.user.id)

        qty = re.total_quantity or 0
        product_quantity = product.quantity or 0

        product.quantity = max(0, int(product_quantity) - qty)

        ca = Cart(
            amount=product.amount,
            quantity=product.quantity,
            payment='null',
            product=product,
            cust=re,
            status='cart'
        )
        ca.save()

        return redirect(request.META['HTTP_REFERER'], {'message': "cart"})


    def post(self, request, *args, **kwargs):
        order_id = request.POST.get('order_id')
        delivery_boy_id = request.POST.get('delivery_boy_id')
        order = Cart.objects.get(id=order_id)
        delivery_boy = User.objects.get(id=delivery_boy_id)
        order.delivery_boy = delivery_boy
        order.save()
        return redirect('delivery_orders')

    
    

class view_cart(TemplateView):
    template_name = 'customer/cartview.html'

    def get_context_data(self, **kwargs):
        context = super(view_cart, self).get_context_data(**kwargs)
        cust = Customer.objects.get(user_id=self.request.user.id)
        cart_items = Cart.objects.filter(status='cart', cust=cust)
        total = sum(int(cart_item.amount) for cart_item in cart_items)

        context['view_cart'] = cart_items
        context['asz'] = total

        return context

from .models import Cart, Customer,Pay
from datetime import datetime

class Payment(TemplateView):
    template_name = 'customer/payment.html'

    def get_context_data(self, **kwargs):
        context = super(Payment, self).get_context_data(**kwargs)
        user = Customer.objects.get(user_id=self.request.user.id)
        cart_items = Cart.objects.filter(status='cart', cust_id=user.id)
        total_amount = sum(float(cart_item.amount) for cart_item in cart_items)

        context['view'] = cart_items
        context['total_amount'] = total_amount

        return context


class chpayment(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        user = Customer.objects.get(user_id=self.request.user.id)
        cart_items = Cart.objects.filter(status='cart', cust_id=user.id)

        total_amount = sum(float(cart_item.amount) for cart_item in cart_items)

        for cart_item in cart_items:
            payment = Pay.objects.create(
                cust=user,
                product=cart_item.product,
                payment_status='paid',
                total_amount=float(cart_item.amount),
                quantity=int(cart_item.quantity),
                payment_date=datetime.now()  # Save the current date and time as the payment date
            )

            cart_item.status = 'paid'
            cart_item.payment = 'paid'
            cart_item.save()

        return render(request, 'customer/index.html', {'message': "Payment success"})
    
    
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
    
    


from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class ChatbotView(View):
    def post(self, request):
        message = request.POST.get('message')
        response_message = self.get_response(message)
        return JsonResponse({'response_message': response_message})

    def get_response(self, message):
        # Your chatbot logic goes here
        if message.lower() in ['hello', 'hi']:
            return "Hello! How can I help you today?"
        elif 'order' in message.lower():
            return "To place an order, please visit our order page."
        else:
            return "I'm sorry, I didn't understand that. Please try again."

    def get(self, request):
        return JsonResponse({'error': 'Invalid request method'}, status=400)

