from django.shortcuts import render, redirect
from .models import USER
from django.contrib import messages
from datetime import datetime
import bcrypt

def index(request):
    # if a user is logged in prevent relogin from a different user because we do not want to overwrite the session data. User needs to log out first then they can go to login.html to login/register
    try: 
        if request.session['userid']:
            context = {"User": USER.objects.get(id=request.session['userid'])}
            return redirect('/wishes')
    except:
        return render(request, 'index.html')

#--------------------------------------------------------
# LOGIN/REGISTRATION
#--------------------------------------------------------
# POST
def register(request):
    if request.method == 'POST':
        errors = USER.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='register')
            return redirect('/')
        else:
            USER.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'].lower(), #email not case sensative
                password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            )
            request.session['userid'] = USER.objects.last().id
            return redirect('/wishes')
    return redirect('/')

# POST
def login(request):
    if request.method == 'POST':
        user = USER.objects.filter(email=request.POST['email'].lower()) #find user with email not case sensative
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                return redirect('/wishes')
        else:
            messages.error(request, "Invalid credentials.", extra_tags='login')
            return redirect('/')
    return redirect('/')

# POST
def logout(request):
    if request.method == 'POST':
        request.session.flush()
    return redirect('/')

#--------------------------------------------------------
# Main
#--------------------------------------------------------
def main(request):
        try: #check if user is logged in
            user = USER.objects.get(id=request.session['userid'])
            context = {
                "User": user,
                # # myWISHES = only include those user created AND not granted
                # "myWISHES": WISH.objects.filter(created_by = user).exclude(granted = True),
                # "grantedWISHES": WISH.objects.filter(granted = True)
                }
            return render(request, 'wishes.html', context)
        except:
            return redirect('/')
    


# AJAX validations for registration page---------------------------------
def register_validations(request, code):
    if request.method == 'POST':
        bad = False
        #code: 0 = first_name, 1 = last_name, 2 = email, 3 = password, 4 = confirm_PW
        if code == 0:
            error = USER.objects.reg_first_name(request.POST)
            if len(error) > 0:
                bad = True
            else:
                error = ''
        elif code == 1:
            error = USER.objects.reg_last_name(request.POST)
            if len(error) > 0:
                bad = True
            else:
                error = ''
        elif code == 2:
            error = USER.objects.reg_email(request.POST)
            if len(error) > 0:
                bad = True
            else:
                error = 'Email available!'
        elif code == 3:
            error = USER.objects.reg_password(request.POST)
            if len(error) > 0:
                bad = True
            else:
                error = 'Strong password!'
        elif code == 4:
            error = USER.objects.reg_confirm_PW(request.POST)
            if len(error) > 0:
                bad = True
            else:
                error = 'Passwords match!'
        context = {
            'bad': bad,
            'error': error
        }
        return render(request, 'partials/reg_validate.html', context)  
    return redirect('/')