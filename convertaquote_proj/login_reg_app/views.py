from django.shortcuts import render, redirect
from .models import CUSTOMER
from django.contrib import messages
from datetime import datetime
import bcrypt

# Login page
def login(request):
    # if a customer is logged in prevent relogin from a different customer because we do not want to overwrite the session data. Customer needs to log out first then they can go to login.html to login/register
    try: 
        if request.session['customerid']:
            context = {"Customer": CUSTOMER.objects.get(id=request.session['customerid'])}
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
            return redirect('/register')
        else:
            CUSTOMER.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'].lower(), #email not case sensative
                password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            )
            request.session['customerid'] = CUSTOMER.objects.last().id
            return redirect('/quote')
    return redirect('/register')

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
            return redirect('/login')
    return redirect('/login')

# POST
def logout(request):
    if request.method == 'POST':
        request.session.flush()
    return redirect('/signin/login')

#--------------------------------------------------------
# Main this should be in other app
#--------------------------------------------------------
def main(request):
        try: #check if customer is logged in
            customer = CUSTOMER.objects.get(id=request.session['customerid'])
            context = {
                "Customer": customer,
                # # myWISHES = only include those customer created AND not granted
                # "myWISHES": WISH.objects.filter(created_by = customer).exclude(granted = True),
                # "grantedWISHES": WISH.objects.filter(granted = True)
                }
            return render(request, 'quote.html', context)
        except:
            return redirect('/quote')
    


# AJAX validations for registration page---------------------------------
def register_validations(request, code):
    if request.method == 'POST':
        bad = False
        #code: 0 = first_name, 1 = last_name, 2 = email, 3 = password, 4 = confirm_PW
        if code == 0:
            error = CUSTOMER.objects.reg_first_name(request.POST)
            if len(error) > 0:
                bad = True
            else:
                error = ''
        elif code == 1:
            error = CUSTOMER.objects.reg_last_name(request.POST)
            if len(error) > 0:
                bad = True
            else:
                error = ''
        elif code == 2:
            error = CUSTOMER.objects.reg_email(request.POST)
            if len(error) > 0:
                bad = True
            else:
                error = 'Email available!'
        elif code == 3:
            error = CUSTOMER.objects.reg_password(request.POST)
            if len(error) > 0:
                bad = True
            else:
                error = 'Strong password!'
        elif code == 4:
            error = CUSTOMER.objects.reg_confirm_PW(request.POST)
            if len(error) > 0:
                bad = True
            else:
                error = 'Passwords match!'
        context = {
            'bad': bad,
            'error': error
        }
        return render(request, 'partials/reg_validate.html', context)  
    return redirect('/register')