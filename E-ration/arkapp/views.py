from django.shortcuts import render,redirect
from . models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import CustomUser, carditem, shopreg
from django.contrib import messages
from django.contrib.auth import get_user_model 
from .models import member 

# Create your views here.


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'index.html')
def home(request):
    return render(request,'index.html')
def customerbase(request):
          return render(request,'customerbase.html')
def shopownerbase(request):
          return render(request,'shopownerbase.html')
def ration(request):
          return render(request,'customer/ration.html')
def customer(request):
          return render(request,'customer.html')
def contact(request):
    return render(request,"contact.html")
def about(request):
          return render(request,"about.html")
def blog(request):
          return render(request,"blog.html")
def collections(request):
          return render(request,"collections.html")      
 
def customersignup(request):
    if request.method == "POST":
        name = request.POST['cname']
        address = request.POST['address']
        phone = request.POST['phone']
        place = request.POST['place']
        houseno = request.POST['houseno']
        membersno = request.POST['membersno']
        user_type = request.POST['type']
        card_color = request.POST['color']
        card_number = request.POST['cnumber']
        email = request.POST['email']
        password = request.POST['password']

        # Get the user model, assuming you have a CustomUser model
        User = get_user_model()

        # Create a new user using the manager's create_user method
        user = User.objects.create_user(username=name, email=email, password=password)

        # Now, set additional attributes for your CustomUser model
        user.name = name
        user.address = address
        user.phone = phone
        user.place = place
        user.houseno = houseno
        user.membersno = membersno
        user.cardtype = user_type
        user.cardcolor = card_color
        user.cardnumber = card_number

        # Save the user
        user.save()

        messages.success(request, 'You have successfully registered!')

    return render(request, "customersignup.html")
      
def shopownersignup(request):
    if request.method == 'POST':
        name = request.POST.get('sname')
        address = request.POST.get('address')
        place = request.POST.get('place')
        phoneno = request.POST.get('phonenumber')
        rationshopno = request.POST.get('shopno')
        liceneceno = request.POST.get('licenceno')
        email = request.POST.get('email')
        password = request.POST.get('password')

        User = get_user_model()  # Use the custom user model manager

        # Create a new user using the custom User model
        usr = User.objects.create_user(username=name, email=email, password=password, last_name="2")

        # Create a new shopreg object and save it
        sst = shopreg(name=name, address=address, place=place, contact_number=phoneno, shop_number=rationshopno, licence=liceneceno, email=email, password=password)
        sst.save()

        messages.success(request, 'You have successfully registered!')

    return render(request, "shopownersignup.html")



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
                        return render(request, 'admin/adminindex.html')
                    elif  user.last_name=='1':
                        details=CustomUser.objects.filter(email=user.email)
                        {'details':details}
                        for i in details:
                                  items=carditem.objects.filter(cardcolor=i.cardcolor)
                                  if i.approve=="approved":
                                            
                                            return render(request, 'customer/customerbase.html',{'items':items})
                                        #return render(request, 'customer.html',{'items':items})
                        messages.error(request, 'Your account has not been approved yet.')             
                    elif user.last_name=='2':
                        shopowner=shopreg.objects.filter(email=user.email)
                        {'shopowner':shopowner}
                        for i in shopowner:
                                  if i.approve=="approved":
                                            return render(request, 'shopownerbase.html')
                        messages.error(request, 'Your account has not been approved yet.')          
                    else:
                        return render(request, 'signin.html' )
                    messages.error(request, 'Invalid username or password.')
              else:
                    return render(request, 'signin.html' )
                    
           return render(request,'signin.html')
                


def viewcustomers(request):
          shop=shopreg.objects.filter(name=request.user.username)
          {'shop':shop}
          for i in shop:
              if CustomUser.objects.filter(place=i.place,approve="approved"):
                        custmain= CustomUser.objects.filter(place=i.place,approve="approved")
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
    itm=CustomUser.objects.filter(name=request.user.username)
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
    if request.method == 'POST':
        cardnumber = request.POST['cardnumber']
        fname = request.POST['fname']
        lname = request.POST['lname']
        age = request.POST['age']
        gender = request.POST['gender']
        occu = request.POST['occupation']
        relation = request.POST['relation']

        mct = member.objects.create(
            customer_name=request.user.username,
            card_number=cardnumber,
            fname=fname,
            lname=lname,
            age=age,
            gender=gender,
            occu=occu,
            relation=relation
        )

    return render(request, "addmembers.html")
                    
                    
                    
                    
    return render(request,"addmembers.html")

def viewmembers(request):
          card=CustomUser.objects.filter(name=request.user.username)
          {'card':card}
          for i in card:
                    itm=member.objects.filter(customer_name=request.user.username,card_number=i.cardnumber,approve='approved')
                    {'items':itm}
                    for i in itm:
                              print(i.customer_name*25)
                    return render(request,'viewmembers.html',{'items':itm})
         
          return render(request,'viewmembers.html')



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
            customer = CustomUser.objects.filter(place=i.place)

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
            if key.startswith('approval_status_'):
                customer_id = key.split('_')[-1]
                customer = CustomUser.objects.get(pk=customer_id)
                customer.approve = value
                customer.save()
        return redirect('customer_list')
    else:
        customers = CustomUser.objects.all()
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





def customer_base_view(request):
    # Query the items you want to display
    items = carditem.objects.all()

    return render(request, 'customer.html', {'items': items})


def ration_price(request):
    # Query the items you want to display
    items = carditem.objects.all()

    return render(request, 'customer/ration.html', {'items': items})

















          
              
              
    
    