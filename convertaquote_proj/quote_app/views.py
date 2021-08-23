from django.shortcuts import render, redirect
from login_reg_app.models import CUSTOMER, SERVICE_ADDRESS
from .models import ITEM_CATEGORY, ITEM_OPTION, ITEM, ADDED_ITEM, QUOTE, ORDER
from django.contrib import messages
from datetime import date, datetime
import json

taxrate = 0.10
deposit = 0.50

def index(request):
    return redirect('/quote')

def quote_page(request):
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
        'subtotal': format(subtotal, ".2f"),
        'tax': format(tax, ".2f"),
        'total': format(total, ".2f")
    }
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
                added_items_array[i]['runningPrice'] = str(format((qty * float(added_items_array[i]['chosenPackgePrice'])), ".2f"))
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
            added_items_array[i]['chosenPackgePrice'] = str(format(packagePrice, ".2f"))
            added_items_array[i]['runningPrice'] = str(format((qty * packagePrice), ".2f"))
            request.session['items_array'] = json.dumps(added_items_array)
            return render(request, 'partials/quoteTable.html', getAllContext(request))
    return redirect('/')

def update_quote_table(request):
    return render(request, 'partials/quoteTable.html', getAllContext(request))

def clear_quote(request):
    request.session['items_array'] = ''
    return redirect('/')

def save(request):
    if request.method == 'POST':
        try: #check if customer is logged in
            customer = CUSTOMER.objects.get(id=request.session['customerid'])
            context = {
                "Customer": customer,
                # # myWISHES = only include those customer created AND not granted
                # "myWISHES": WISH.objects.filter(created_by = customer).exclude(granted = True),
                # "grantedWISHES": WISH.objects.filter(granted = True)
                }
            return render(request, 'savequote.html', context)
        except:
            return redirect('/signin/login')
    return redirect('/')

def saving(request):
    if request.method == 'POST':
        try:
            createQuoteFromSession(request, request.POST['quoteName'])
            return redirect('/quote/savedquotes')
        except:
            return redirect('/signin/login')
    print('about to redirect to "/"')
    return redirect('/')

def createQuoteFromSession(request, quoteName):
    customer_curr = CUSTOMER.objects.get(id=request.session['customerid'])
    added_items_array = json.loads(request.session['items_array']) 
    QUOTE.objects.create(
        name = quoteName,
        customer = customer_curr
    )
    for dict in added_items_array:
        ADDED_ITEM.objects.create(
                item = ITEM.objects.get(id=dict['id']),
                qty = dict['qty'],
                package = dict['package'],
                customer = customer_curr
            )
        ADDED_ITEM.objects.last().quotes.add(QUOTE.objects.last())
    return QUOTE.objects.last().id

def savedquotes(request):
    context = {'Quotes': CUSTOMER.objects.get(id=request.session['customerid']).quotes.all()}
    return render(request, 'savedQuotes.html', context)

def editquote(request, quoteID):
    quote = QUOTE.objects.get(id=quoteID)
    added_items_fromQuote = quote.added_items.all()
    added_items_array = []
    for added_item in added_items_fromQuote:
        itemm = added_item.item
        added_items_array.append({
            'id': itemm.id,
            'qty': added_item.qty,
            'package': added_item.package,
            'category':itemm.category.name,
            'name_Long':itemm.name_Long, 
            'name_short':itemm.name_short,
            'price_basic': str(itemm.price_basic),
            'price_add_plus':str(itemm.price_add_plus),
            'price_add_pro': str(itemm.price_add_pro),
            'runningPrice': str(itemm.price_basic),
            'chosenPackgePrice': str(itemm.price_basic),
            })
    request.session['items_array'] = '' # clear existing quote in session first
    request.session['items_array'] = json.dumps(added_items_array)
    return redirect('/quote/')

def destroyQuote(request, quoteID):
    if request.method == 'POST':
        quote = QUOTE.objects.get(id=quoteID)
        quote.delete()
    return redirect('/quote/savedquotes')

def account(request):
    try: #check if customer is logged in
        customer = CUSTOMER.objects.get(id=request.session['customerid'])
        context = {"customer": customer}
        return render(request, 'myaccount.html', context)
    except:
        return redirect('/signin/login')

# THIS needs validations!
def schedule(request):
    try: #check if customer is logged in
        if CUSTOMER.objects.get(id=request.session['customerid']):
            try:
                if request.session['items_array']: 
                    return render(request, 'schedule.html', getAllContext(request)) 
            except:
                return redirect('/')
    except:
        return redirect('/signin/login')

def scheduling(request):
    if request.method == 'POST':
        try: #check if customer is logged in
            if CUSTOMER.objects.get(id=request.session['customerid']):
                request.session['service_date'] = request.POST['serviceDate']
                request.session['service_time'] = request.POST['serviceTime']
                return redirect('/quote/address')
        except:
            return redirect('/signin/login')
    return redirect('/')

def address(request):
    try: #check if customer is logged in
        customer = CUSTOMER.objects.get(id=request.session['customerid'])
        context = {"customer": customer}
        return render(request, 'address.html', context)
    except:
        return redirect('/signin/login')

def setaddress(request):
    if request.method == 'POST':
        try: 
            if CUSTOMER.objects.get(id=request.session['customerid']):
                request.session['currentServAddressID'] = request.POST['selectedAddressID']
                return redirect('/quote/revieworder')
        except:
            return redirect('/signin/login')
    return redirect('/')

def revieworder(request):
    try: #check if customer is logged in
        customer = CUSTOMER.objects.get(id=request.session['customerid'])
        
        date = datetime.strptime(request.session['service_date'],'%Y-%m-%d') # parse YYYY-MM-DD
        time = datetime.strptime(request.session['service_time'],'%H:%M') # parse HH:MM (24hr clock)
        dateFormated = date.strftime("%A, %B %-d %Y") #https://strftime.org
        timeFormated = time.strftime("%-I:%M %p") 
        context = getAllContext(request)
        context["customer"] = customer
        context["service_date"] = dateFormated
        context["service_time"]  =timeFormated
        context["service_address"] = SERVICE_ADDRESS.objects.get(id=request.session['currentServAddressID'])
        return render(request, 'revieworder.html', context)
    except:
        return redirect('/signin/login')

def submitorder(request):
    if request.method == 'POST':
        # try: 
            data = getAllContext(request) #check if customer is logged in
            total = float(data['total'])
            quoteID = createQuoteFromSession(request, datetime.now().strftime('%Y-%m-%d_%H:%M'))
            print(total)
            print(deposit)
            ORDER.objects.create(
                service_date = request.session['service_date'],
                service_time = request.session['service_time'],
                paid_amount = total * deposit,
                due_amount = total - (total * deposit),
                service_address = SERVICE_ADDRESS.objects.get(id=request.session['currentServAddressID']),
                quote = QUOTE.objects.get(id=quoteID)
            )
            ORDER.objects.last()
            # once an order is generated delete this session data
            del request.session['service_date']
            del request.session['service_time']
            del request.session['currentServAddressID']
            return redirect('/quote/receipt')
        # except:
        #     return redirect('/signin/login')
    return redirect('/')

def receipt(request):
    return render(request, 'receipt.html', {'Order' : ORDER.objects.last()} )

def billing(request):
    return redirect('/')







def manage_address(request):
    return redirect('/')