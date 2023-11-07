from django.contrib import admin
from .models import itemlist, CustomUser, shopreg, customerdetails, items, carditem, member, booking

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'cardnumber', 'email', 'approve')
    list_filter = ('approve',)
    search_fields = ('name', 'email')

@admin.register(itemlist)
class ItemListAdmin(admin.ModelAdmin):
    list_display = ('item',)

# Define admin classes for other models (shopreg, customerdetails, items, carditem, member, booking)
