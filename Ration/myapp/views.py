from django.shortcuts import render,redirect
from . models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile
# Create your views here.


def home(request):
    return render(request,'home.html')
def customerbase(request):
          return render(request,'customerbase.html')
def adminbase(request):
          return render(request,'adminbase.html')      
def customer(request):
          return render(request,'customer.html')      
def shopowner(request):
          return render(request,'shopowner.html')  
def admincustomer_list(request):
          return render(request,'admincustomer_list.html')   
def adminshopowner_list(request):
          return render(request,'adminshopowner_list.html')                     
def contact(request):
    return render(request,"contact.html")
def blog(request):
          return render(request,"blog.html")
def ration(request):
          return render(request,'ration.html')       
def admincustomer_list(request):
          return render(request,'admincustomer_list.html')     

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from .models import custreg

def customersignup(request):
    if request.method == "POST":
        name = request.POST['cname']
        address = request.POST['address']
        place = request.POST['place']
        membersno = request.POST['membersno']
        type = request.POST['type']
        color = request.POST['color']
        cardnumber = request.POST['cnumber']
        email = request.POST['email']
        password = request.POST['password']

        # Check if the username already exists
        if User.objects.filter(username=name).exists():
            messages.error(request, 'Username is not available. Please choose another.')
            return render(request, "customersignup.html")

        # Create a new user
        user = User.objects.create_user(username=name, email=email, password=password, last_name="1")

        try:
            ration_card_file = request.FILES['ration_card']
            # Save the file to the ration_card field
            fs = FileSystemStorage()
            filename = fs.save(ration_card_file.name, ration_card_file)
        except MultiValueDictKeyError:
            messages.error(request, 'Ration card file is required.')
            return render(request, "customersignup.html")

        # Create a new customer registration entry
        customer = custreg()
        customer.name = name
        customer.address = address
        customer.place = place
        customer.membersno = membersno
        customer.cardtype = type
        customer.cardcolor = color
        customer.cardnumber = cardnumber
        customer.email = email
        customer.password = password
        customer.ration_card = fs.url(filename)  # Save the file URL to the model
        customer.save()

        messages.success(request, 'You have successfully registered!')
        return redirect("signin.html")

    return render(request, "customersignup.html")

      
      
def shopownersignup(request):
          if request.method=='POST':
                    name=request.POST['sname']
                    address=request.POST['address']
                    place=request.POST['place']
                    phoneno=request.POST['phonenumber']
                    rationshopno=request.POST['shopno']
                    liceneceno=request.POST['licenceno']
                    email=request.POST['email']
                    password=request.POST['password']     
                    sst=shopreg()
                    sst.name=name
                    sst.address=address
                    sst.place=place
                    sst.contact_number=phoneno
                    sst.shop_number=rationshopno
                    sst.licence=liceneceno
                    usr=User.objects._create_user(username=name,email=email,password=password,last_name="2")
                    usr.save() 
                    sst.email=email
                    sst.password=password
                    sst.save()
                    messages.success(request, 'You have successfully registered!')
          return render(request,"shopownersignup.html" )
  
      
def signin(request):
           if request.method=='POST':
              name=request.POST['name']
              password=request.POST['password']
              print(name)
              print(password)
              user = authenticate(username=name, password=password)
              if user is not None:
                    login(request,user)
                    if user.is_superuser:
                        return render(request, 'adminbase.html')
                    elif  user.last_name=='1':
                        details=custreg.objects.filter(email=user.email)
                        {'details':details}
                        for i in details:
                                  items=carditem.objects.filter(cardcolor=i.cardcolor)
                                  if i.approve=="approved":
                                            
                                            return render(request, 'customerbase.html',{'items':items})
                        messages.error(request, 'Your account has not been approved yet.')             
                    elif user.last_name=='2':
                        shopowner=shopreg.objects.filter(email=user.email)
                        {'shopowner':shopowner}
                        for i in shopowner:
                                  if i.approve=="approved":
                                            return render(request, 'shopowner.html')
                        messages.error(request, 'Your account has not been approved yet.')          
                    else:
                        return render(request, 'signin.html' )
                    messages.error(request, 'Invalid username or password.')
              else:
                    return render(request, 'signin.html' )
                    
           return render(request,'signin.html')
                

def logout_view(request):
    logout(request)
    return render(request,'home.html')




def viewcustomers(request):
          shop=shopreg.objects.filter(name=request.user.username)
          {'shop':shop}
          for i in shop:
              if custreg.objects.filter(place=i.place,approve="approved"):
                        custmain= custreg.objects.filter(place=i.place,approve="approved")
                        return render(request,'viewcustomers.html',{'customers':custmain})           
          return render(request,'viewcustomers.html')
      

          
 

def addstock(request):
          if request.method=="POST":
                    item=request.POST['itemname']
                    quant=request.POST['quantity']
                    if items.objects.filter(shopowner=request.user.username,item=item):
                              items.objects.filter(item=item,shopowner=request.user.username).update(item=item,shopowner=request.user.username,quantity=quant)
                    else:
                              items.objects.filter(item=item).create(item=item,shopowner=request.user.username,quantity=quant)
                    
        
          itm=itemlist.objects.all()  
          return render(request,"addstock.html",{'items':itm})
      
def viewstock(request):
          itm=items.objects.filter(shopowner=request.user.username)
          return render(request,'viewstock.html',{'items':itm})
      
def viewcuststock(request):
    itm=custreg.objects.filter(name=request.user.username)
    {"itm":itm}
    for i in itm:
              print(i.place)
    shop=shopreg.objects.filter(place=i.place)
    {'shop':shop}
    for j in shop:
              print(j.place)
    
    stocklist=items.objects.filter(shopowner=j.name)
    return render(request,'viewcuststock.html',{'stocklist':stocklist})

def addmembers(request):
          if request.method=='POST':
                    print(request.method)
                    cardnumber=request.POST['cardnumber']
                    fname=request.POST['fname']
                    lname=request.POST['lname']
                    age=request.POST['age']
                    gender=request.POST['gender']
                    occu=request.POST['occupation']
                    relation=request.POST['relation']
                    print(fname,lname)
                        
                    mct=member()
                    mct.customer_name=request.user.username
                    mct.card_number=cardnumber
                    
                    mct.fname=fname
                    mct.lname=lname
                    mct.age=age
                    mct.gender=gender
                    mct.occu=occu
                    mct.relation=relation
                    mct.save()
                    
                    
                    
                    
                    
          return render(request,"addmembers.html")

def viewmembers(request):
          card=custreg.objects.filter(name=request.user.username)
          {'card':card}
          for i in card:
                    itm=member.objects.filter(customer_name=request.user.username,card_number=i.cardnumber,approve='approved')
                    {'items':itm}
                    for i in itm:
                              print(i.customer_name*25)
                    return render(request,'viewmembers.html',{'items':itm})
         
          return render(request,'viewmembers.html')
      
      
      
      
def purchese(request):
          if request.method=="POST":
                    name=request.POST.get('itemname')
                    qnt=request.POST.get('quant')
                    rate=request.POST.get('rate')
                    time=request.POST['times']
                    print(name * 50)
                    card=custreg.objects.filter(name=request.user.username)
                    {'cards':card}
                    for i in card:
                              print(i.place)
                              shop=shopreg.objects.filter(place=i.place)
                              {'shop':shop}
                              for j in shop:
                                        print(j.shop_number)
                                        
                                        bk=booking()
                                        bk.pickup_time=time
                                        bk.item=name
                                        bk.quantity=qnt
                                        bk.rate=rate
                                        bk.card_number=i.cardnumber
                                        bk.shop_number=j.shop_number
                                        bk.customer_name=request.user.username
                                        bk.save()
                                        
                                    
                    
                    
          details=custreg.objects.filter(email=request.user.email)
          {'details':details}
          for i in details:
                    items=carditem.objects.filter(cardcolor=i.cardcolor)
                    if i.approve=="approved":
                            return render(request, 'purchase.html',{'items':items})
          
          return render(request,'purchase.html')
      


def history(request):
          customer=custreg.objects.filter(name=request.user.username)
          {'customer':customer}
          for i in customer:
                    book=booking.objects.filter(card_number=i.cardnumber)
          return render(request,'history.html',{'books':book})
      
# views.py



def shophistory(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('status'):
                booking_id = key.replace('status', '')
                status = value

                if booking_id:
                    booking_obj = booking.objects.get(id=booking_id)
                    booking_obj.status = status
                    booking_obj.save()

            elif key == 'delete':
                booking_id = value

                if booking_id:
                    booking.objects.filter(id=booking_id).delete()

        return redirect('shophistory')
    else:
        owner = shopreg.objects.filter(name=request.user.username)
        customer_list = []

        for i in owner:
            customer = custreg.objects.filter(place=i.place)

            for j in customer:
                book = booking.objects.filter(card_number=j.cardnumber, shop_number=i.shop_number)

                for k in book:
                    customer_list.append({
                        'id': k.id,
                        'customer_name': k.customer_name,
                        'card_number': k.card_number,
                        'item': k.item,
                        'quantity': k.quantity,
                        'rate': k.rate,
                        'booking_date': k.booking_date,
                        'pickup_time': k.pickup_time,
                        'status': k.status
                    })

    return render(request, 'shophistory.html', {'book': customer_list})


def shoptiming(request):
          return render(request,"shoptimimg.html")
def custtiming(request):
          return render(request,"custtiming.html")
      




def customer_list(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            print(f'Key: {key}, Value: {value}')
            if key.startswith('approval_status_'):
                customer_id = key.split('_')[-1]
                customer = custreg.objects.get(pk=customer_id)
                customer.approve = value
                customer.save()
        return redirect('customer_list')
    else:
        customers = custreg.objects.all()
        return render(request, 'admincustomer_list.html', {'customers': customers})


def shopowner_list(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('approval_status_'):
                shop_id = key.split('_')[-1]
                shop_owner = shopreg.objects.get(pk=shop_id)
                shop_owner.approve = value
                shop_owner.save()
        return redirect('shopowner_list')
    else:
        shop_owners = shopreg.objects.all()
        return render(request, 'adminshopowner_list.html', {'shop_owners': shop_owners})
    


def member_list(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('approval_status_'):
                member_id = key.split('_')[-1]
                member_obj = member.objects.get(pk=member_id)
                member_obj.approve = value
                member_obj.save()
        return redirect('member_list')
    else:
        members = member.objects.filter(approve='pending')
        return render(request, 'adminmember_list.html', {'members': members})


    
def viewmember_list(request):
          members = member.objects.filter(approve='approved')
          return render(request, 'admin_view_member.html', {'members': members})
      



def admin_stock(request):
    items_data = items.objects.all()
    return render(request, 'admin_stock.html', {'items': items_data})



def admin_item(request):
    if request.method == 'POST':
        item = request.POST['item']
        new_item = itemlist(item=item)
        new_item.save()
         
    return render(request, 'admin_item.html')






def add_carditem(request):
    if request.method == 'POST':
        cardcolor = request.POST['cardcolor']
        item_id = request.POST['item']
        quantity = request.POST['quantity']
        rate = request.POST['rate']
        item = itemlist.objects.get(id=item_id)
        card_item = carditem(cardcolor=cardcolor, item=item, quantity=quantity, rate=rate)
        card_item.save()
        return redirect('admin_view_carditem')

    else:
        items = itemlist.objects.all()
        return render(request, 'admin_carditem.html', {'items': items})







def admin_view_carditem(request):
    if request.method == 'POST':
        carditem_id = request.POST.get('carditem_id')
        if carditem_id:
            carditem_obj = carditem.objects.get(id=carditem_id)
            carditem_obj.delete()
            return redirect('admin_view_carditem')

    carditems = carditem.objects.all()
    context = {'carditems': carditems}
    return render(request, 'admin_view_carditem.html', context)


      





def view_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        if item_id:
            item = itemlist.objects.get(pk=item_id)
            item.delete()
            return redirect('view_item')

    items = itemlist.objects.all()
    return render(request, 'admin_item_view.html', {'items': items})

from django.shortcuts import render
from .models import carditem

def shopcarditem(request):
    card_items = carditem.objects.all()
    return render(request, 'shopcarditem.html', {'carditems': card_items})



def deactivate_user(request, user_id):
    user = get_object_or_404(customer, id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
         # Send deactivation email
        subject = 'Account Deactivation'
        message = 'Your account has been deactivated by the admin.'
        from_email = 'erationshop1@gmail.com'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('deactivation_mail.html', {'user': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)

    else:
        messages.warning(request, f"User '{user.username}' is already deactivated.")
    return redirect('admin.html')

def activate_user(request, user_id):
    user = get_object_or_404(customer, id=user_id)
    if not user.is_active:
        user.is_active = True
        user.save()
        subject = 'Account activated'
        message = 'Your account has been activated.'
        from_email = 'erationshop1@gmail.com'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('activation_mail.html', {'user': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)
    else:
        messages.warning(request, f"User '{user.username}' is already active.")
    return redirect('admin.html')

# myapp/views.py


def edit_profile_view(request, user):
    user = get_object_or_404(UserProfile, id=user)

    if request.method == 'POST':
        # Update user fields directly from request.POST
        user.cname = request.POST.get('cname')
        user.address = request.POST.get('address')
        user.place = request.POST.get('place')
        user.houseno = request.POST.get('houseno')
        user.membersno = request.POST.get('membersno')
        user.cnumber = request.POST.get('cnumber')
        user.type = request.POST.get('type')
        user.color = request.POST.get('color')
        user.email = request.POST.get('email')

        # Handle file upload for the ration_card
        if 'ration_card' in request.FILES:
            user.ration_card = request.FILES['ration_card']

        # Update the password if provided
        password = request.POST.get('password')
        if password:
            user.password = password

        user.save()
        # Add a success message if needed
        return redirect('index')  # Replace 'index' with the name of the view where you want to redirect

    return render(request, 'edit_profile.html', {'user': user})
















          
              
              
    
    