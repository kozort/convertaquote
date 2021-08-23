from django.urls import path
from . import views

app_name = 'quote'
urlpatterns = [
    path('', views.quote_page,),
    path('new', views.quote_page, name="new_quote"),
    path('schedule', views.schedule, name="schedule"),
    path('scheduling', views.scheduling, name="scheduling"),
    path('address', views.address, name="address"),
    path('setaddress', views.setaddress, name="setaddress"),
    path('revieworder', views.revieworder,  name="revieworder"),
    path('submitorder', views.submitorder,  name="submitorder"),
    path('receipt', views.receipt,  name="receipt"),
    path('billing', views.billing, name="billing"),

    path('clear', views.clear_quote,  name="clear_quote"),
    path('save', views.save,  name="save_quote"),
    path('saving', views.saving,  name="saving_quote"),
    path('savedquotes', views.savedquotes,  name="savedquotes"),
    path('delete/<int:quoteID>', views.destroyQuote,  name="destroyQuote"),
    path('edit/<int:quoteID>', views.editquote, name="edit_quote"),

    path('myaccount', views.account,  name="account"),
    path('manage_address', views.manage_address,  name="manage_address"),

    # AJAX to select a service and put it in session and then to table
    path('pickitem/<int:itemID>', views.pick_item,  name="pickitem"),
    path('updateitem/<int:itemID>/remove', views.remove_item,  name="removeitem"),
    path('updateitem/<int:itemID>', views.update_item,  name="updateitem"),
    path('updateitem/package/<str:package>/<int:itemID>', views.update_item_package,  name="updateitempackage"),
    path('updatequotetable', views.update_quote_table,  name="updateQuoteTable")
]
