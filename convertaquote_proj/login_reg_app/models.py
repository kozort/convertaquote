from django.db import models
# from datetime import datetime, timedelta
import re

class CustomerManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        # run all the functions and sum all the errors into one dictionary
        # The keys in 'errors' need to be empty if no errors
        f = self.reg_first_name(postData)
        if len(f) > 0:
            errors["first_name"] = f
        l = self.reg_last_name(postData)
        if len(l) > 0:
            errors["last_name"] = l
        e = self.reg_email(postData)
        if len(e) > 0:
            errors["email"] = e
        p = self.reg_password(postData)
        if len(p) > 0:
            errors["password"] = p
        c = self.reg_confirm_PW(postData)
        if len(c) > 0:
            errors["confirm_PW"] = c
        return errors

    # these are broken out seperately for ajax calls:
    def reg_first_name(self, postData):
        error = ''
        if len(postData['first_name']) < 2:
            error = "First Name should be at least 2 characters"
        return error

    def reg_last_name(self, postData):
        error = ''
        if len(postData['last_name']) < 2:
            error = "Last Name should be at least 2 characters"
        return error

    def reg_email(self, postData):
        error = ''
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            error = ("Invalid email address.")
        if len(CUSTOMER.objects.filter(email=postData['email'].lower())) > 0:
            error = "Email already taken, email should be unique"
        return error

    def reg_password(self, postData):
        error = ''
        if len(postData['password']) < 8:
            more = 8-len(postData['password'])
            error = f"Weak Password! Password should be {more} more characters."
        return error

    def reg_confirm_PW(self, postData):
        error = ''
        if postData['confirm_PW'] != postData['password']:
            error = "Passwords need to match."
        return error

class CUSTOMER(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)

    primaryPhone = models.CharField(max_length=15)
    secondaryPhone = models.CharField(max_length=15)

    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #addresses = list of SERVICE_ADDRESS'es that the customer can order service on
    #added_items = list of items and quantities the customer added to a quote
    #quotes = list of quotes the customer created

    objects = CustomerManager()

    def __str__(self):
        return f"{self.first_name}, {self.last_name}"


class AddressManager(models.Manager):
    def address_validator(self, postData):
        errors = {}
        # run all the functions and sum all the errors into one dictionary
        # The keys in 'errors' need to be empty if no errors
        return errors


class SERVICE_ADDRESS(models.Model):

    address = models.CharField(max_length=45)
    address2 = models.CharField(max_length=45, blank=True)
    state = models.CharField(max_length=2)
    zipcode = models.IntegerField()

    customer = models.ForeignKey(CUSTOMER, related_name="addresses", on_delete=models.CASCADE) #a customer who this ervice address belongs to
    # orders = lists which orders the address is used on

    objects = AddressManager()

    def __str__(self):
        return f"{self.address}, {self.address2}, {self.state}, {self.zipcode}"