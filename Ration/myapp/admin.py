from django.contrib import admin
from . models import *

class custregfields(admin.ModelAdmin):
      list_display=('name','cardnumber','address','place','membersno','approve')
class customerdetailsfields(admin.ModelAdmin):
      list_display=('name','cardnumber','shopowner','cardtype','cardcolor')
class itemsfields(admin.ModelAdmin):
      list_display=('item','shopowner','quantity')
class carditemfields(admin.ModelAdmin):
      list_display=('cardcolor','item','quantity','rate')
class memberfields(admin.ModelAdmin):
      list_display=('customer_name','card_number','fname','lname','age','gender','occu','relation','approve')
class bookingfields(admin.ModelAdmin):
      list_display=('customer_name','shop_number','card_number','item','quantity','rate','booking_date','pickup_time')
class shopregfields(admin.ModelAdmin):
      list_display=('name','address','email','password','licence','shop_number','contact_number','place','approve')
admin.site.register(custreg,custregfields)
admin.site.register(shopreg,shopregfields)
admin.site.register(items,itemsfields)
admin.site.register(customerdetails,customerdetailsfields)
admin.site.register(itemlist)
admin.site.register(carditem,carditemfields)
admin.site.register(member,memberfields)
admin.site.register(booking,bookingfields)



# Register your models here.
