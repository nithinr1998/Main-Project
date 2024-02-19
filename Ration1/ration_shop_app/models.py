from django.db import models
from django.contrib.auth.models import User, AbstractUser
# Create your models here.

class UserType(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    type = models.CharField(max_length=50,null=True)
    
class Card(models.Model):
    card = models.CharField(max_length=20, null=True)
    allowed_quantity=models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)
    
class Product_Item(models.Model):
    item = models.CharField(max_length=20, null=True)
    status = models.CharField(max_length=100, null=True)
    
class Product(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE,null=True)
    item = models.ForeignKey(Product_Item, on_delete=models.CASCADE,null=True)
    quantity = models.CharField(max_length=1000, null=True)
    arrived = models.DateField( auto_now_add=False, null=True)
    amount = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)
    
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    item = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE,null=True)
    card_number = models.CharField(max_length=11, null=True)
    contact = models.CharField(max_length=15, null=True)
    email = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=100, null=True)
    total_quantity=models.CharField(max_length=100, null=True)
    
class Shop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    license = models.CharField(max_length=10, null=True)
    mobile = models.CharField(max_length=15, null=True)
    email = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=100, null=True)
    
class Member(models.Model):
    cust = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=15, null=True)
    relation = models.CharField(max_length=11, null=True)
    age = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=15, null=True)
    job = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)

class Cart(models.Model):
    cust = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    payment = models.CharField(max_length=30,null=True)
    status = models.CharField(max_length=30,null=True)
    amount=models.CharField(max_length=30,null=True)
    quantity = models.CharField(max_length=1000, null=True)

class UserType(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=100, null=True)
    contact_number = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=100, null=True)
    vehicle_type = models.CharField(max_length=50, null=True)
    registration_number = models.CharField(max_length=50, null=True)
    delivery_zones = models.CharField(max_length=100, null=True)
    availability_timings = models.CharField(max_length=100, null=True)