from django.conf.urls import include
from django.urls import path
from . import views
urlpatterns = [
    path('custreg/', views.custreg, name='Custregister'),
    path('appt/', views.appt, name='Appt'),
]
