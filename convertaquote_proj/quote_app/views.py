from django.shortcuts import render, redirect
from login_reg_app.models import CUSTOMER, SERVICE_ADDRESS
from .models import ITEM_CATEGORY, ITEM_OPTION, ITEM, ADDED_ITEM, QUOTE, ORDER, RECEIPT
from django.contrib import messages
from datetime import datetime
import json

taxrate = 0.10

def index(request):
    return redirect('/quote')

def quote_page(request):
    print('quote page')
    added_items_array = []
    try:
        if request.session['items_array']: 
            return render(request, 'new_quote.html', getAllContext(request)) 
    except:
        pass
    context = {
        "Categories": ITEM_CATEGORY.objects.all(),
        "Items": ITEM.objects.all(),
        }
    return render(request, 'new_quote.html', context)

def getAllContext(request):
    added_items_array = json.loads(request.session['items_array']) 
    subtotal = 0.00
    for dict in added_items_array:
        subtotal += float(dict['runningPrice'])
    tax = subtotal * taxrate
    total = subtotal + tax
    context = {
        "Categories": ITEM_CATEGORY.objects.all(),
        "Items": ITEM.objects.all(),
        'Added': added_items_array,
        'Categories_Added': populate_categories(added_items_array),
        'subtotal': subtotal,
        'tax': tax,
        'total': total
    }
    # print all context
    # for cat in context['Categories']:
    #     print(f'Categories: ', cat)

    # for items in context['Items']:
    #     print(f'Items: ', items)

    # for Added in context['Added']:
    #     for k, v in Added.items():
    #         print(f'{k}: {v}')

    # for Categories_Added in context['Categories_Added']:
    #     print(f'Categories_Added: ', Categories_Added)
    return context

def populate_categories(dict_array):
    categories_added_list = []
    for dict in dict_array:
        if not dict['category'] in categories_added_list:
            categories_added_list.append(dict['category'])
    return categories_added_list

#AJAX
def pick_item(request, itemID):
    added_items_array = []
    try:
        if request.session['items_array']: #check if session has anything, if it does not then it is first time use; it will error and move to 'except' line
            added_items_array = json.loads(request.session['items_array']) # if items_array already exsists in session then copy it over to our variable
            # check if the item we clicked on already exists, if it does then do nothing, user needs to use table to update/delete
            for dict in added_items_array:
                if dict['id'] == itemID:
                    #change nothing, put the context back and just return
                    return render(request, 'partials/optionsTable.html', getAllContext(request)) 
            # if we completed the loop and did not return the html page then the item is not in the array
    except:
        pass
    # create new dictionary to add to array
    itemm = ITEM.objects.get(id=itemID)
    added_items_array.append({
        'id': itemID,
        'qty':1, #defualt quantity=1 
        'package':'Basic', #defualt package=basic
        'category':itemm.category.name,
        'name_Long':itemm.name_Long, 
        'name_short':itemm.name_short,
        'price_basic': str(itemm.price_basic),
        'price_add_plus':str(itemm.price_add_plus),
        'price_add_pro': str(itemm.price_add_pro),
        'runningPrice': str(itemm.price_basic),
        'chosenPackgePrice': str(itemm.price_basic),
        }) #its better to add all this stuff here through one query
    request.session['items_array'] = json.dumps(added_items_array) #serialize and add to session array so that we can access it the next time around
    return render(request, 'partials/optionsTable.html', getAllContext(request))

def remove_item(request, itemID):
    added_items_array = json.loads(request.session['items_array'])
    # find and delete the item that matches id
    for i in range(len(added_items_array)):
        if added_items_array[i]['id'] == itemID:
            del added_items_array[i]
            break
    # put array back in session for next time
    request.session['items_array'] = json.dumps(added_items_array) #serialize and add to session array so that we can access it the next time around
    return render(request, 'partials/optionsTable.html', getAllContext(request))

def update_item(request, itemID):
    if request.method == 'POST':
        added_items_array = json.loads(request.session['items_array'])
        for i in range(len(added_items_array)):
            if added_items_array[i]['id'] == itemID:
                qty = int(request.POST[f'qtySelect{itemID}'])
                added_items_array[i]['qty'] = qty
                added_items_array[i]['runningPrice'] = str(qty * float(added_items_array[i]['chosenPackgePrice']))
                request.session['items_array'] = json.dumps(added_items_array)
                # context = {
                #     "Categories": ITEM_CATEGORY.objects.all(),
                #     "Items": ITEM.objects.all(),
                #     'Added': added_items_array
                #     }
                # return render(request, 'partials/quoteTable.html', context)
    return redirect('/')

def update_item_package(request, package, itemID):
    added_items_array = json.loads(request.session['items_array'])
    for i in range(len(added_items_array)):
        if added_items_array[i]['id'] == itemID:
            qty = int(added_items_array[i]['qty'])
            added_items_array[i]['package'] = package
            packagePrice = float(added_items_array[i]['price_basic'])
            if package == 'Basic':
                pass
            elif package == 'Plus':
                packagePrice += float(added_items_array[i]['price_add_plus'])
            elif package == 'Pro':
                packagePrice += float(added_items_array[i]['price_add_plus']) + float(added_items_array[i]['price_add_pro'])
            added_items_array[i]['chosenPackgePrice'] = str(packagePrice)
            added_items_array[i]['runningPrice'] = str(qty * packagePrice)
            request.session['items_array'] = json.dumps(added_items_array)
            return render(request, 'partials/quoteTable.html', getAllContext(request))
    return redirect('/')

def update_quote_table(request):
    return render(request, 'partials/quoteTable.html', getAllContext(request))

def clear_quote(request):
    request.session['items_array'] = ''
    print(request.session['items_array'])
    return redirect('/')

def save(request):
    if request.method == 'POST':
        pass
    return redirect('/')

def schedule(request):
    if request.method == 'POST':
        pass
    return redirect('/')

def address(request):
    return redirect('/')

def revieworder(request):
    return redirect('/')

def billing(request):
    return redirect('/')

def savedquotes(request):
    return redirect('/')



def account(request):
    return redirect('/')

def manage_address(request):
    return redirect('/')