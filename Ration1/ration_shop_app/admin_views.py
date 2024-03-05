from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View
from django.core.mail import EmailMessage
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import Max

from ration_shop_app.models import Card, Customer, Product, Product_Item, Shop,UserType


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
        fe = Card()
        fe.card= card
        fe.status ='card added'
        fe.save()
        return render(request, 'admin/index.html', {'message': "Card Successfully added"})
    
class AddProduct(TemplateView):
    template_name = 'admin/products.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
    
    def post(self, request, *args, **kwargs):
        item_name = request.POST.get('item', '')
        image_file = request.FILES.get('image', None)

        if image_file:
            # Save the image file to the media directory
            file_name = default_storage.save('product_images/' + image_file.name, ContentFile(image_file.read()))
            image_path = 'media/' + file_name
        else:
            image_path = None

        reg = Product_Item(item=item_name, image=image_path)
        reg.status = 'Product added'
        reg.save()

        return render(request, 'admin/index.html', {'message': "Product successfully added"})

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
    
class ApprovedShopListView(TemplateView):
    template_name = 'admin/Approvedshop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shops = Shop.objects.filter(user__last_name='1', user__is_staff='0')
        context['shops'] = shops
        return context
    

class AddDeliveryBoy(View):
    def get(self, request, *args, **kwargs):
        delivery_boys = UserType.objects.filter(type="Delivery")
        locations = Shop.objects.values_list('location', flat=True).distinct()
        return render(request, 'admin/add_delivery_boy.html', {'delivery_boys': delivery_boys,'locations': locations})

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        name = request.POST['name']
        contact_number = request.POST['contact_number']
        address = request.POST['address']
        vehicle_type = request.POST['vehicle_type']
        delivery_zones = request.POST['delivery_zones']
        availability_timings = request.POST['availability_timings']

        # Generate a random password for the delivery boy
        password = User.objects.make_random_password()
        
        # Get the maximum registration number currently in the database
        max_registration_number = UserType.objects.aggregate(Max('registration_number'))['registration_number__max']
        
        # If there are no existing registration numbers, start from 1, else increment the maximum by 1
        if max_registration_number:
            new_registration_number = str(int(max_registration_number) + 1).zfill(6)  # Ensure 6 digits
        else:
            new_registration_number = '000001'
        
        # Create a user with the provided email and generated password
        user = User.objects.create_user(username=email, password=password, first_name=name, email=email,
                                            is_staff='0', last_name='1')
        

        # Create a UserType object for the delivery boy with the new registration number
        user_type = UserType.objects.create(
            user=user,
            type="Delivery",
            name=name,
            contact_number=contact_number,
            address=address,
            vehicle_type=vehicle_type,
            registration_number=new_registration_number,
            delivery_zones=delivery_zones,
            availability_timings=availability_timings
        )

        # Send an email to the delivery boy with their password
        subject = 'Your account details for the delivery service'
        message = f'Email: {email}\nPassword: {password}'
        email = EmailMessage(subject, message, to=[email])
        email.send()

        # Get updated list of delivery boys
        delivery_boys = UserType.objects.filter(type="Delivery")
        
        return render(request, 'admin/add_delivery_boy.html', {'message': 'Delivery boy added successfully', 'delivery_boys': delivery_boys})
    
class DeliveryBoyHistoryView(View):
    def get(self, request, *args, **kwargs):
        delivery_boys = UserType.objects.filter(type="Delivery")
        return render(request, 'admin/Delivery_Boys.html', {'delivery_boys': delivery_boys})
    
    def post(self, request, *args, **kwargs):
        delivery_boy_id = request.POST.get('id')
        reason = request.POST.get('reason')
        
        if delivery_boy_id:
            try:
                delivery_boy = UserType.objects.get(id=delivery_boy_id)
                delivery_boy.delete()
                message = f"Delivery boy {delivery_boy_id} deleted successfully. Reason: {reason}"
            except UserType.DoesNotExist:
                message = f"Delivery boy {delivery_boy_id} not found."
        else:
            message = "Delivery boy ID not provided."
        
        delivery_boys = UserType.objects.filter(type="Delivery")
        return render(request, 'admin/Delivery_Boys.html', {'delivery_boys': delivery_boys, 'message': message})