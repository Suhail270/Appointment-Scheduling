from django.conf.urls import include
from django.urls import path
from . import views
urlpatterns = [

    path('<slug:slug>/customer_reg/', views.customer_reg, name='customer_reg'),
    # path('customer_reg/appointment.html',views.appointment, name='appointment'),
]

