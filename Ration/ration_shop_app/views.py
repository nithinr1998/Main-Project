from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView

from ration_shop_app.models import Card, Customer, Shop,UserType
# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'
    
class TimeView(TemplateView):
    template_name = 'shoptiming.html'
    
class Customer_RegView(TemplateView):
    template_name = 'cust_reg.html'  
    
    def get_context_data(self, **kwargs):
        context = super(Customer_RegView, self).get_context_data(**kwargs)
        card = Card.objects.all()
        context['card'] = card
        return context 

    def post(self, request, *args, **kwargs):
        card = request.POST['card']
        name = request.POST['name']
        card_number =request.POST['card_number']
        email = request.POST['email']
        contact = request.POST['contact']
        address = request.POST['address']
        location = request.POST['location']
        password = request.POST['password']

        if User.objects.filter(email=email):
            print('pass')
            return render(request, 'cust_reg.html', {'message': "already added the username or email"})

        else:
            user = User.objects.create_user(username=email, password=password, first_name=name, email=email,
                                            is_staff='0', last_name='0')
            user.save()
            reg = Customer()
            reg.card_id = card
            reg.user = user
            reg.card_number =card_number
            reg.contact = contact   
            reg.address = address 
            reg.location = location    
            reg.password = password
            reg.save()
            usertype = UserType()
            usertype.user = user
            usertype.type = "customer"
            usertype.save()
            # messages="Registered Successfully"

            return render(request, 'index.html', {'message': "successfully added"})
        
class Shop_RegView(TemplateView):
    template_name = 'shop_reg.html'   

    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        license =request.POST['license']
        email = request.POST['email']
        mobile = request.POST['mobile']
        address = request.POST['address']
        location = request.POST['location']
        password = request.POST['password']

        if User.objects.filter(email=email):
            print('pass')
            return render(request, 'cust_reg.html', {'message': "already added the username or email"})

        else:
            user = User.objects.create_user(username=email, password=password, first_name=name, email=email,
                                            is_staff='0', last_name='0')
            user.save()
            reg = Shop()
            reg.user = user
            reg.license =license
            reg.mobile = mobile  
            reg.address = address 
            reg.location = location      
            reg.password = password
            reg.save()
            usertype = UserType()
            usertype.user = user
            usertype.type = "shop"
            usertype.save()
            # messages="Registered Successfully"

            return render(request, 'index.html', {'message': "successfully added"})
        
class loginview(TemplateView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            if user.last_name == '1':
                if user.is_superuser:
                    return redirect('/admin')
                elif UserType.objects.get(user_id=user.id).type == "customer":
                    return redirect('/customer')
                elif UserType.objects.get(user_id=user.id).type == "shop":
                    return redirect('/shop')
            else:
                return render(request, 'login.html', {'message': " User Account Not Authenticated"})


        else:
            return render(request, 'login.html', {'message': "Invalid Username or Password"})
        
        
        