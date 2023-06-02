from django.conf.urls import include
from django.urls import path
from . import views
from .views import appointmentsListView

urlpatterns = [
    path('register/', views.register, name='register'),
<<<<<<< HEAD
    #path('appointments/', views.update_appointment_status, name = "appointments"),
    path('update_appointment/', views.update_appointment_status, name='update_appointment_status'),
    path('delete_appointment/', views.delete_appointment_status, name='delete_appointment_status'),
    path('appointment/', views.appointment_api),
    # path('agents/', views.agent_api, name = "agents")
=======
    # path('appointments/', appointmentsListView.as_view())
    path('update_appointment/', views.update_appointment_status, name='update_appointment_status')
>>>>>>> 3591df04cb4716d68720de5b2ee5421f1782c6c3
]
