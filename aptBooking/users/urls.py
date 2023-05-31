from django.conf.urls import include
from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path("add/", views.add, name="add"),
    path("hello/", views.say_hello, name="hello"),
]
