from django.conf.urls import include
from django.urls import path
from . import views
# from .views import appointmentsListView

urlpatterns = [
    path('<slug:slug>/register/', views.register, name='register'),
    # path('appointments/', appointmentsListView.as_view())
    # path('update_appointment/', views.update_appointment_status, name='update_appointment_status'),
    path('delete_appointment/', views.delete_appointment_status, name='delete_appointment_status'),
    path('search_appointment/', views.search_demo, name='search_appointment_status'),

]
