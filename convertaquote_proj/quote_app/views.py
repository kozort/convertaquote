from django.shortcuts import render, redirect
from login_reg_app.models import CUSTOMER, SERVICE_ADDRESS
from .models import ITEM_CATEGORY, ITEM_OPTION, ITEM, ADDED_ITEM, QUOTE, ORDER, RECEIPT
from django.contrib import messages
from datetime import datetime
import json

def index(request):
    return redirect('/quote')

def quote_page(request):
    added_items_array = []
    try:
        if request.session['items_array']: 
            added_items_array = json.loads(request.session['items_array']) 
            context = {
                "Categories": ITEM_CATEGORY.objects.all(),
                "Items": ITEM.objects.all(),
                'Added': added_items_array
                }
            return render(request, 'new_quote.html', context) 
    except:
        context = {
            "Categories": ITEM_CATEGORY.objects.all(),
            "Items": ITEM.objects.all(),
            }
        return render(request, 'new_quote.html', context)


#AJAX
def pick_item(request, itemID):
    print('entered pick_item')
    added_items_array = []
    try:
        if request.session['items_array']: #check if session has anything, if it does not then it is first time use; it will error and move to 'except' line
            added_items_array = json.loads(request.session['items_array']) # if items_array already exsists in session then copy it over to our variable
            # check if the item we clicked on already exists, if it does then do nothing, user needs to use table to update/delete
            for dict in added_items_array:
                if dict['id'] == itemID:
                    #change nothing, put the context back and just return
                    context = {
                        "Categories": ITEM_CATEGORY.objects.all(),
                        "Items": ITEM.objects.all(),
                        'Added': added_items_array
                        }
                    return render(request, 'partials/optionsTable.html', context) 
            # if we completed the loop and did not return the html page then the item is not in the array
    except:
        pass
    # create new dictionary to add to array
    itemm = ITEM.objects.get(id=itemID)
    added_items_array.append({
        'id': itemID,
        'qty':1, #defualt quantity=1 
        'package':1, #defualt package=1(basic)
        'name_Long':itemm.name_Long, 
        'name_short':itemm.name_short,
        'price_basic': str(itemm.price_basic),
        'price_add_plus':str(itemm.price_add_plus),
        'price_add_pro': str(itemm.price_add_pro)
        }) #its better to add all this stuff here through one querry 
    request.session['items_array'] = json.dumps(added_items_array) #serialize and add to session array so that we can access it the next time around
    context = {
        "Categories": ITEM_CATEGORY.objects.all(),
        "Items": ITEM.objects.all(),
        'Added': added_items_array
        }
    return render(request, 'partials/optionsTable.html', context)

def remove_item(request, itemID):
    added_items_array = json.loads(request.session['items_array'])
    # find and delete the item that matches id
    for i in range(len(added_items_array)-1):
        if added_items_array[i]['id'] == itemID:
            del added_items_array[i]
    # put array back in session for next time
    request.session['items_array'] = json.dumps(added_items_array) #serialize and add to session array so that we can access it the next time around
    context = {
        "Categories": ITEM_CATEGORY.objects.all(),
        "Items": ITEM.objects.all(),
        'Added': added_items_array
        }
    return render(request, 'partials/optionsTable.html', context)

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