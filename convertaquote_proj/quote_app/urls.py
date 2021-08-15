from django.urls import path
from . import views

urlpatterns = [
    path('', views.quote_page,),
    path('new', views.quote_page, name="new_quote"),
    path('schedule', views.schedule, name="schedule"),
    path('address', views.address, name="address"),
    path('revieworder', views.revieworder,  name="revieworder"),
    path('billing', views.billing, name="billing"),

    path('save', views.save,  name="save_quote"),
    path('savedquotes', views.savedquotes,  name="savedquotes"),

    path('account', views.account,  name="account"),
    path('manage_address', views.manage_address,  name="manage_address"),
]