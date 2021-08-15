from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('registering', views.registering, name="registering"),
    path('logining', views.logining, name="logining"),
    path('logout', views.logout,  name="logout"),
    # validations for registration page
    path('reg_validate/<int:code>', views.register_validations,  name="reg_validate"),

    # validations for registration page
    # path('address_val/<int:code>', views.address_validations,  name="address_val")
]
