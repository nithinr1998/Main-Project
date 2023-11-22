from django.db import models

# Create your models here.
class itemlist(models.Model):
      item=models.CharField(max_length=20)
      def __str__(self):
            return self.item
      
class custreg(models.Model):
    name = models.CharField(max_length=50)
    cardnumber = models.IntegerField(unique=True)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    address = models.CharField(max_length=50, default='address')
    place = models.CharField(max_length=50, default='place')
    membersno = models.IntegerField(default=0)
    cardcolor = models.CharField(max_length=10)  # Update this line
    ration_card = models.FileField(upload_to='ration_cards/', null=True, blank=True)
    approve = models.CharField(max_length=50, default='declined')
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
      customer_name=models.CharField(max_length=10)
      card_number=models.IntegerField(default=0)
      fname=models.CharField(max_length=50)
      lname=models.CharField(max_length=50)
      age=models.IntegerField()
      gender=models.CharField(max_length=50)
      occu=models.CharField(max_length=50)
      relation=models.CharField(max_length=50)
      approve=models.CharField(max_length=50, default='decline')
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

      # myapp/models.py

from django.db import models

class UserProfile(models.Model):
    cname = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    place = models.CharField(max_length=100)
    houseno = models.IntegerField()
    membersno = models.IntegerField()
    cnumber = models.IntegerField()
    type = models.CharField(max_length=3, choices=[('1', 'Choose Card'), ('APL', 'APL'), ('BPL', 'BPL')])
    color = models.CharField(max_length=10, choices=[('1', 'Choose Color'), ('White', 'White'), ('Blue', 'Blue'), ('Pink', 'Pink'), ('Yellow', 'Yellow')])
    email = models.EmailField()
    ration_card = models.FileField(upload_to='ration_cards/')
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.cname
