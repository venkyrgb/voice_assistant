from django.urls import path
from .views import *
app_name = 'src'

urlpatterns = [
    
    path('' , home , name = 'home'),
    path('login/' , login_page , name = 'login'),
    path("register/", register_page, name="register"),
    path("logout/", logout_page, name="logout"),
    path('start_assitant/' , start_assitant , name="start_assitant")



]   
