from django.shortcuts import render, redirect
from login_reg_app.models import CUSTOMER, SERVICE_ADDRESS
from .models import ITEM_CATEGORY, ITEM_OPTION, ITEM, ADDED_ITEM, QUOTE, ORDER, RECEIPT
from django.contrib import messages
from datetime import datetime

def index(request):
    return redirect('/quote')

def quote_page(request):
    return render(request, 'new_quote.html')

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


