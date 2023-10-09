from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='loginpage')
def index(request):
    # Pass the logged-in user's username to the template
    username = request.user.username if request.user.is_authenticated else None
    return render(request, 'index.html', {'username': username})

def index(request):
    return render(request,'index.html')

def collections(request):
     return render(request,'collections.html')
 
def loginn(request):
    if request.method == "POST":   
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        
        if user:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('loginpage')
    
    return render(request, 'loginpage.html')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if User.objects.filter(email=email).exists():
            messages.info(request, "Email already exists")
            return redirect('Registrationpage')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'registrationpage.html', {'error': 'Passwords do not match'})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('loginpage')
    else:
        return render(request, 'Registrationpage.html')

def blog(request):
     return render(request,'blog.html') 
 
def contact(request):
     return render(request,'contact.html') 
 
def customer_update(request):
    if request.method == "POST":
        username = request.POST['username']
        cname = request.POST['cname']
        email = request.POST['email']
        address = request.POST['address']
        place = request.POST['place']
        wardno = int(request.POST['wardno'])  # Convert to int
        houseno = int(request.POST['houseno'])  # Convert to int
        membersno = int(request.POST['membersno'])  # Convert to int
        cnumber = int(request.POST['cnumber'])  # Convert to int
        card_type = request.POST['type']
        card_color = request.POST['color']
        zipcode = request.POST['zipcode']
        

        # Create an instance of the Customer model and populate it with the data
        customer = customer_update(username=username,cname=cname,email=email,address=address,place=place,houseno=houseno,membersno=membersno,cnumber=cnumber,card_type=card_type,card_color=card_color,zipcode=zipcode )

        # Save the customer data to the database
        customer.save()

        return render(request, 'update.html')

    return render(request, 'update.html') 

 
def logout(request):
     auth.logout(request)
     request.session.clear()
     return redirect('/')