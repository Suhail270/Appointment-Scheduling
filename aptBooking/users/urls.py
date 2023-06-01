from django.conf.urls import include
from django.urls import path
from . import views
from .views import appointmentsListView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('appointments/', appointmentsListView.as_view())
]
