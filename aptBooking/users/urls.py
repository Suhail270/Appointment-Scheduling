from django.conf.urls import include
from django.urls import path
from .views import appointmentsListView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    #path('appointments/', views.update_appointment_status, name = "appointments"),
    path('appointments/', appointmentsListView.as_view()),
    path('agents/', views.agent_api, name = "agents")
]

