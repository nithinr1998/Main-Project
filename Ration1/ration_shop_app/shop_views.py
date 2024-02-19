from urllib import request
from django.contrib.auth.models import User
from django.views.generic import TemplateView, View
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from ration_shop_app.models import Card, Cart, Customer, Member, Product, Product_Item

class Indexview(TemplateView):
    template_name = 'shop/index.html'

class NewCustView(TemplateView):
    template_name = 'shop/customer_list.html'

    def get_context_data(self, **kwargs):
        context = super(NewCustView, self).get_context_data(**kwargs)
        user = User()
        cards =Card.objects.all()
        customer = Customer.objects.filter(
            user__last_name='0', user__is_staff='0')
        context['users'] = user
        context['cards'] = cards
        context['customer'] = customer
        return context

class AddedMemberView(TemplateView):
    template_name = 'shop/approvemember.html'

    def get_context_data(self, **kwargs):
        context = super(AddedMemberView, self).get_context_data(**kwargs)
        
        member = Member.objects.filter(status = "added")
        
        context['member'] = member
        return context
    
class ApproveView(View):
    def dispatch(self, request, *args, **kwargs):

        id = request.GET['id']
        user = User.objects.get(pk=id)
        user.last_name = '1'
        user.save()
        return render(request, 'shop/index.html', {'message': " Account Approved"})


class RejectView(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        user = User.objects.get(pk=id)
        user.last_name = '2'
        user.is_active = '0'
        user.save()
        return render(request, 'shop/index.html', {'message': "Account Removed"})
    

class CustView(TemplateView):
    template_name = 'shop/registeredcustlist.html'

    def get_context_data(self, **kwargs):
        context = super(CustView, self).get_context_data(**kwargs)
        # user = User()
        customer = Customer.objects.filter(
            user__last_name='1', user__is_staff='0')
        # context['users'] = user
        context['customer'] = customer
        return context
    
# class ApprovedmemberView(TemplateView):
#     template_name = 'shop/approvedmemberlist.html'
    
#     def get_context_data(self, **kwargs):
#         id1=self.request.user.id
#         cus = Customer.objects.get(id=id1)
#         context = super(ApprovedmemberView, self).get_context_data(**kwargs)
        
#         # cust=self.request.user.id
#         mem = Member.objects.filter(user_id=cus.id)
#         context['mem'] = mem
#         return context
class ApprovedmemberView(TemplateView):
    template_name = 'shop/approvedmemberlist.html'
    
    def get_context_data(self, **kwargs):
        context = super(ApprovedmemberView, self).get_context_data(**kwargs)
        id=self.request.GET['id']
        view1 = Member.objects.filter(cust_id=id,status='Approved')
        cu=Customer.objects.get(id=id)
        context['view1'] = view1
        context['count']=cu
        return context
    def post(self, request, *args, **kwargs):
        id3 = request.POST['id']
        quantity = request.POST['qu']
        d=Customer.objects.get(id=id3)
        d.total_quantity=quantity
        d.save()
        return render(request, 'shop/index.html',{'message': "total quantity of product required for this card added successfully"})

        
    
    
    
class AddProduct(TemplateView):
    template_name = 'shop/addproductstock.html' 
    
    def get_context_data(self, **kwargs):
        context = super(AddProduct, self).get_context_data(**kwargs)
        card = Card.objects.all()
        item = Product_Item.objects.all()
        context['card'] = card
        context['item'] = item
        return context 
    
    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.request.user.id)
        item = request.POST['item']
        quantity = request.POST['quantity']
        arrived = request.POST['arrived']
        amount = request.POST['amount']
        card = request.POST['card']
        month = request.POST['month']  # Retrieve month value
        
        reg = Product()
        
        reg.user = user
        reg.item_id = item
        reg.quantity = quantity
        reg.arrived = arrived
        reg.amount = amount
        reg.card_id = card
        reg.month = month  # Assign month value to the model field
        reg.status = 'added'
        reg.save()
        
        return render(request, 'shop/index.html', {'message': "product successfully added "})
    
from datetime import datetime

class View_Product(TemplateView):
    template_name = 'shop/productslist.html'

    def get_context_data(self, **kwargs):
        context = super(View_Product, self).get_context_data(**kwargs)

        # Retrieve filter parameters from the request
        card_id = self.request.GET.get('card', '')
        month = self.request.GET.get('month', '')

        # Get all cards for the dropdown
        context['cards'] = Card.objects.all()

        # Filter products based on selected card and month
        products = Product.objects.all()
        if card_id:
            products = products.filter(card_id=card_id)
        if month:
            # Filter products by the month part of the arrived date
            products = products.filter(arrived__month=int(month))

        context['view_pp'] = products
        return context
    
    
class Member_Approve_Request(View):
    
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        user = Member.objects.get(pk=id)
        user.status = "Approved"
        user.save()
        return render(request, 'shop/index.html', {'message': " Member approved"})
    
class Member_Reject_Request(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        user = Member.objects.get(pk=id)
        user.status = 'Rejected'
        user.save()
        return render(request, 'shop/index.html', {'message': "Member Rejected"})
    
class Reject(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        Product.objects.get(id=id).delete()
        return redirect(request.META['HTTP_REFERER'])
    
class View_confirmed_order(TemplateView):
    template_name = 'shop/view_order_placed.html'

    def get_context_data(self, **kwargs):
        # user = User.objects.get(user_id=self.request.user.id)

        pro = Cart.objects.filter(payment='paid')
        context = {
            'pro': pro,
        }
        return context


from django.views.generic import ListView
from django.db.models import Q

class HistoryListView(ListView):
    model = Product
    template_name = 'shop/history.html'
    context_object_name = 'history_items'

    def get_queryset(self):
        queryset = Product.objects.all()
        month = self.request.GET.get('month')
        card = self.request.GET.get('card')

        if month:
            queryset = queryset.filter(arrived__month=month)

        return queryset
