from django.db import models
# from datetime import datetime, timedelta
from login_reg_app.models import CUSTOMER, SERVICE_ADDRESS
import re

class ITEM_CATEGORY(models.Model):
    name = models.CharField(max_length=45)
    #items = the items that are in this category

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ITEM_OPTION(models.Model):
    name = models.CharField(max_length=45) #naming convention should be itemName_package (ex. carpetRoom_basic, or hallway_pro)
    description = models.CharField(max_length=255)
    price_unit = models.DecimalField(max_digits=7, decimal_places=2)
    #items = the items that have this option

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ITEM(models.Model):
    name = models.CharField(max_length=45)
    category = models.ForeignKey(ITEM_CATEGORY, related_name="items", on_delete=models.CASCADE)
    options = models.ManyToManyField(ITEM_OPTION, related_name="items") #up to three options per item allowed: 1=basic, 2=plus, 3=pro
    #line_item = the added_item this item is on, which include the qty of this item and the selected package

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ADDED_ITEM(models.Model):
    item = models.ForeignKey(ITEM, related_name="line_item", on_delete=models.CASCADE)
    qty = models.IntegerField(max_length=4)
    package = models.IntegerField(max_length=1) #package type is identified numerically, 1=basic, 2=plus, 3=pro
    #quotes = the quotes this line item is on

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class QUOTE(models.Model):
    added_items = models.ManyToManyField(ADDED_ITEM, related_name="quotes") #the line items on this quote

    # orders = lists which orders these quotes are copied to
    customer = models.ForeignKey(CUSTOMER, related_name="quotes", on_delete=models.CASCADE) #customer can have many saved quotes

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ORDER(models.Model):
    service_date = models.DateField()
    service_time = models.TimeField()
    
    service_address = models.ForeignKey(SERVICE_ADDRESS, related_name="orders", on_delete=models.CASCADE) #service_addresses can be on multiple orders, such as when a customer has multiple properties
    quote = models.ForeignKey(QUOTE, related_name="orders", on_delete=models.CASCADE) # the quote that was issused to this order (quotes can be on multiple orders with reoccuring service)
    # receipt = order is paid for and on a reciept

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class RECEIPT(models.Model):
    paid_date_time = models.DateTimeField()
    paid_amount = models.DecimalField(max_digits=7, decimal_places=2)
    due_amount = models.DecimalField(max_digits=7, decimal_places=2)
    
    order = models.OneToOneField(ORDER, related_name="receipt", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
