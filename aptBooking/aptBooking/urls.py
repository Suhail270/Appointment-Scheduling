"""aptBooking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views as user_views
from django.conf.urls import include
from django.views.generic.base import TemplateView 
from django.contrib.auth.views import LoginView
from sales.views import AppointmentCreateView, AppointmentUpdateView, get_available_time_slots, AppointmentCancelView

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('register/',user_views.register, name='register'),
    path('users/', include('django.contrib.auth.urls')),
    path('users/',include('users.urls')),


    path('sales/', include('django.contrib.auth.urls')),
    path('sales/',include('sales.urls')),


    path('', TemplateView.as_view(template_name='dashboard.html'), name='home'),
    #path('login/', LoginView.as_view(), name='login')

    path('', TemplateView.as_view(template_name='dashboard.html'), name='home'),
    #path('login/', LoginView.as_view(), name='login')
    path('appointments/create/', AppointmentCreateView.as_view(), name='apt-create'),
    path('appointments/update/<int:pk>/', AppointmentUpdateView.as_view(), name='apt-update'),
    path('appointments/cancel/<int:pk>/', AppointmentCancelView.as_view(), name='apt-cancel'),
    path("get_available_time_slots/", get_available_time_slots, name="get_available_time_slots")

]
