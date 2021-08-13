from django.urls import path
from . import views

urlpatterns = [
    # login and dashboard
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    # validations for registration page
    path('reg_validate/<int:code>', views.register_validations)
]
