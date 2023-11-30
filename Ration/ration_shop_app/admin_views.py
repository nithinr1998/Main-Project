from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View

from ration_shop_app.models import Card, Customer, Product, Product_Item, Shop

class Indexview(TemplateView):
    template_name = 'admin/index.html'
    
class NewShopView(TemplateView):
    template_name = 'admin/shop_list.html'

    def get_context_data(self, **kwargs):
        context = super(NewShopView, self).get_context_data(**kwargs)
        user = User()
        shop = Shop.objects.filter(
            user__last_name='0', user__is_staff='0')
        context['users'] = user
        context['shop'] = shop
        return context
    
class ApproveView(View):
    def dispatch(self, request, *args, **kwargs):

        id = self.request.GET['id']
        user = User.objects.get(pk=id)
        user.last_name = '1'
        user.save()
        return render(request, 'admin/index.html', {'message': " Account Approved"})


class RejectView(View):
    def dispatch(self, request, *args, **kwargs):
        id = self.request.GET['id']
        user = User.objects.get(pk=id)
        user.last_name = '2'
        user.is_active = '0'
        user.save()
        return render(request, 'admin/index.html', {'message': "Account Rejected"})
    
class AddCard(TemplateView):
    template_name = 'admin/card.html'   

    def post(self, request, *args, **kwargs):

        card = request.POST['card']
        allowed_quantity = request.POST['allowed_quantity']
        fe = Card()
        fe.card= card
        fe.allowed_quantity=allowed_quantity
        fe.status ='card added'
        fe.save()
        return render(request, 'admin/index.html', {'message': "Card Successfully added"})
    
class AddProduct(TemplateView):
    template_name = 'admin/products.html' 
    
    def post(self, request, *args, **kwargs):
        
        item = request.POST['item']      
        reg = Product_Item()       
        reg.item = item
        reg.status='Product added'
        reg.save()
        
        return render(request, 'admin/index.html', {'message': "product successfully added "})

class View_Product(TemplateView):
    template_name = 'admin/productsView.html'
    def get_context_data(self, **kwargs):
        context = super(View_Product, self).get_context_data(**kwargs)
        view = Product_Item.objects.all()
        context['view'] = view
        return context
    
class CustView(TemplateView):
    template_name = 'admin/customer_list.html'

    def get_context_data(self, **kwargs):
        context = super(CustView, self).get_context_data(**kwargs)
        user = User()
        customer = Customer.objects.filter(
            user__last_name='1', user__is_staff='0')
        context['users'] = user
        context['customer'] = customer
        return context
    
class Reject(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        Product_Item.objects.get(id=id).delete()
        return redirect(request.META['HTTP_REFERER'])