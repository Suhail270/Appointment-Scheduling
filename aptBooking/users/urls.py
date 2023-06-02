from django.conf.urls import include
from django.urls import path
from .views import appointmentsListView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    #path('appointments/', views.update_appointment_status, name = "appointments"),
    path('update_appointment/', views.update_appointment_status, name='update_appointment_status'),
    path('delete_appointment/', views.delete_appointment_status, name='delete_appointment_status'),
    path('appointment/', views.appointment_api),
    # path('agents/', views.agent_api, name = "agents")
]

