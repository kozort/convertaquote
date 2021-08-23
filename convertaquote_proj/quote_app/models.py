from django.db import models
# from datetime import datetime, timedelta
from login_reg_app.models import CUSTOMER, SERVICE_ADDRESS
import re

# created only by admin user
class ITEM_CATEGORY(models.Model):
    name = models.CharField(max_length=45)
    #items = the items that are in this category

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

# created only by admin user
class ITEM_OPTION(models.Model):
    name = models.CharField(max_length=45) #naming convention should be itemName_package (ex. carpetRoom_basic, or hallway_pro)
    description = models.CharField(max_length=255)

    category = models.ForeignKey(ITEM_CATEGORY, related_name="options", on_delete=models.CASCADE, null=True)
    #items = the items that have this option

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category.name}: {self.name}"

# created only by admin user
class ITEM(models.Model):
    name_short = models.CharField(max_length=45)
    name_Long = models.CharField(max_length=90, blank=True)
    price_basic = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    price_add_plus = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    price_add_pro = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    
    category = models.ForeignKey(ITEM_CATEGORY, related_name="items", on_delete=models.CASCADE)
    options = models.ManyToManyField(ITEM_OPTION, related_name="items", blank=True) #up to three options per item allowed: 1=basic, 2=plus, 3=pro
    #on_line_items = the added_item this item is on, which include the qty of this item and the selected package

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name_short}"

# created by customer when quote is created
class ADDED_ITEM(models.Model):
    item = models.ForeignKey(ITEM, related_name="on_line_items", on_delete=models.CASCADE)
    qty = models.IntegerField()
    package = models.CharField(max_length=45) #package name here is only one of three: 'basic', 'plus', 'pro'
    #quotes = the quotes this line item is on
    customer = models.ForeignKey(CUSTOMER, related_name="added_items", on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Item:{self.item.name_short}, QTY: {self.qty}, package:{self.package}"

# created by customer and app. The quotes that belong to a reciept will be hidden so that the customer can't delete them
class QUOTE(models.Model):
    name = models.CharField(max_length=95, null=True)
    added_items = models.ManyToManyField(ADDED_ITEM, related_name="quotes", blank=True) #the line items on this quote

    # orders = lists which orders these quotes are copied to
    customer = models.ForeignKey(CUSTOMER, related_name="quotes", on_delete=models.CASCADE) #customer can have many saved quotes

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} for: {self.customer.first_name}"

# created by the app
class ORDER(models.Model):
    service_date = models.DateField()
    service_time = models.TimeField()
    paid_amount = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    due_amount = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    
    service_address = models.ForeignKey(SERVICE_ADDRESS, related_name="orders", on_delete=models.CASCADE) #service_addresses can be on multiple orders, such as when a customer has multiple properties
    quote = models.ForeignKey(QUOTE, related_name="orders", on_delete=models.CASCADE) # the quote that was issused to this order (quotes can be on multiple orders with reoccuring service)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} for: {self.quote.customer.first_name}"

