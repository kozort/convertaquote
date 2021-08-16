from django.shortcuts import render, redirect
from login_reg_app.models import CUSTOMER, SERVICE_ADDRESS
from .models import ITEM_CATEGORY, ITEM_OPTION, ITEM, ADDED_ITEM, QUOTE, ORDER, RECEIPT
from django.contrib import messages
from django.contrib.sessions.serializers import JSONSerializer
# from django.http import JsonResponse
from datetime import datetime

def index(request):
    return redirect('/quote')

def quote_page(request):
    context = {
        "Categories": ITEM_CATEGORY.objects.all(),
        "Items": ITEM.objects.all(),
        "AddedItems": ADDED_ITEM.objects.all(),
        }
    return render(request, 'new_quote.html', context)

def pick_item(request, itemID):
    try:
        request.session[f'{itemID}']
    except:
        request.session[f'{itemID}'] = itemID
        request.session[f'qty{itemID}'] = 1
        request.session[f'package{itemID}'] = 1
        return render(request, 'partials/optionsTable.html')
    return redirect('/quote')

def update_item(request, added_itemID):
    pass

def schedule(request):
    return redirect('/')

def address(request):
    return redirect('/')

def revieworder(request):
    return redirect('/')

def billing(request):
    return redirect('/')

def savedquotes(request):
    return redirect('/')

def save(request):
    return redirect('/')

def account(request):
    return redirect('/')

def manage_address(request):
    return redirect('/')