from django.shortcuts import render, redirect
from .models import CUSTOMER, SERVICE_ADDRESS
from django.contrib import messages
from datetime import datetime
import bcrypt

# Login page
def login(request):
    # if a customer is logged in prevent relogin from a different customer because we do not want to overwrite the session data. Customer needs to log out first then they can go to login.html to login/register
    try: 
        if request.session['customerid']:
            context = {"Customer": CUSTOMER.objects.get(id=request.session['customerid'])}
            print(request.session['customerid'])
            return redirect('/quote/myaccount')
    except:
        return render(request, 'login.html')

# Register page
def register(request):
    # if a customer is logged in prevent relogin from a different customer because we do not want to overwrite the session data. CUSTOMER needs to log out first then they can go to login.html to login/register
    try: 
        if request.session['customerid']:
            context = {"Customer": CUSTOMER.objects.get(id=request.session['customerid'])}
            return redirect('/quote/myaccount')
    except:
        return render(request, 'register.html')
#--------------------------------------------------------
# LOGIN/REGISTRATION
#--------------------------------------------------------
# POST
def registering(request):
    if request.method == 'POST':
        errors = CUSTOMER.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='register')
            return redirect('/signin/register')
        else:
            CUSTOMER.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'].lower(), #email not case sensitive
                password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            )
            SERVICE_ADDRESS.objects.create(
                address = request.POST['address'],
                address2 = request.POST['address2'],
                state = request.POST['state'],
                zipcode = request.POST['zipcode'],
                customer = CUSTOMER.objects.last()
            )
            request.session['customerid'] = CUSTOMER.objects.last().id
            return redirect('/quote')
    return redirect('/signin/register')

# POST
def logining(request):
    if request.method == 'POST':
        customer = CUSTOMER.objects.filter(email=request.POST['email'].lower()) #find customer with email not case sensative
        if customer:
            logged_customer = customer[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_customer.password.encode()):
                request.session['customerid'] = logged_customer.id
                return redirect('/quote')
        else:
            messages.error(request, "Invalid credentials.", extra_tags='login')
            return redirect('/signin/login')
    return redirect('/signin/login')

# POST
def logout(request):
    del request.session['customerid']
    return redirect('/signin/login')
    


# AJAX validations for registration page---------------------------------
def register_validations(request, code):
    if request.method == 'POST':
        bad = False
        divID = ''
        #code: 0 = first_name, 1 = last_name, 2 = email, 3 = password, 4 = confirm_PW
        if code == 0:
            error = CUSTOMER.objects.reg_first_name(request.POST)
            if len(error) > 0:
                bad = True
            else:
                error = ''
            divID = 'first_name'
        elif code == 1:
            error = CUSTOMER.objects.reg_last_name(request.POST)
            if len(error) > 0:
                bad = True
            else:
                error = ''
            divID = 'last_name'
        elif code == 2:
            error = CUSTOMER.objects.reg_email(request.POST)
            if len(error) > 0:
                bad = True
            else:
                error = 'Email available!'
            divID = 'email'
        elif code == 3:
            error = CUSTOMER.objects.reg_password(request.POST)
            if len(error) > 0:
                bad = True
            else:
                error = 'Strong password!'
            divID = 'password'
        elif code == 4:
            error = CUSTOMER.objects.reg_confirm_PW(request.POST)
            if len(error) > 0:
                bad = True
            else:
                error = 'Passwords match!'
            divID = 'confirm_PW'
        context = {
            'bad': bad,
            'error': error,
            'divID': divID
        }
        print(context['error'])
        return render(request, 'partials/reg_validate.html', context)  
    return redirect('/register')