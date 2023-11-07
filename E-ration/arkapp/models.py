from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.
class itemlist(models.Model):
      item=models.CharField(max_length=20)
      def __str__(self):
            return self.item
      
class CustomUser(AbstractUser):
      name = models.CharField(max_length=255)
      cardnumber = models.CharField(max_length=16)
      email = models.EmailField(unique=True)  # Use email as the unique identifier
      password=models.CharField(max_length=50)
      address=models.CharField(max_length=50,default='address')
      place=models.CharField(max_length=50,default='place')
      houseno=models.IntegerField(default=0)
      membersno=models.IntegerField(default=0)
      cardtype=models.CharField(max_length=50,default='type')
      cardcolor=models.CharField(max_length=50,default='color')
      phoneno=models.IntegerField(default=0)
      approve=models.CharField(max_length=50,default='declined')
      def __str__(self):
            return self.name
      
      
class shopreg(models.Model):
      name=models.CharField(max_length=50)
      address=models.CharField(max_length=50,default="address")
      email=models.CharField(max_length=50)
      password=models.CharField(max_length=50)
      licence=models.CharField(max_length=50,default="licence number")
      shop_number=models.CharField(max_length=50,default='shop number',unique=True)
      contact_number=models.IntegerField(default=0)
      place=models.CharField(max_length=50,default='place')
      approve=models.CharField(max_length=50,default='declined')
      def __str__(self):
            return self.name
class customerdetails(models.Model):
      shopowner=models.CharField(max_length=50,default="shopowner")
      name=models.CharField(max_length=50)
      cardnumber=models.IntegerField()
      cardtype=models.CharField(max_length=10)
      cardcolor=models.CharField(max_length=10)
class items(models.Model):
      item=models.CharField(max_length=20)
      shopowner=models.CharField(max_length=25,default="shopowner")
      quantity=models.IntegerField(default=0)
class carditem(models.Model):
      cardcolor=models.CharField(max_length=10)
      item=models.ForeignKey(itemlist,on_delete=models.CASCADE)
      quantity=models.IntegerField()
      rate=models.IntegerField()
class member(models.Model):
     customer_name = models.CharField(max_length=255)
     card_number = models.CharField(max_length=255)
     fname = models.CharField(max_length=255)
     lname = models.CharField(max_length=255)
     age = models.IntegerField()
     gender = models.CharField(max_length=10)
     occu = models.CharField(max_length=255)
     relation = models.CharField(max_length=255)
     approve = models.CharField(max_length=50, default='decline')
     def __str__(self):
        return self.fname + ' ' + self.lname
class booking(models.Model):
      customer_name=models.CharField(max_length=50)
      shop_number=models.CharField(max_length=50)
      card_number=models.IntegerField()
      item=models.CharField(max_length=20)
      quantity=models.IntegerField()
      rate=models.IntegerField()
      booking_date=models.DateField(auto_now=True)
      pickup_time=models.TimeField()
      status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'approved'), ('delivered', 'delivered')], default='pending')

      