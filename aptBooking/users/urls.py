from django.urls import path
from . import views 

#URLConf
urlpatterns = [
    path("add/", views.add, name='add'),
    path("hello/", views.say_hello, name='hello'),
    
]