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

from users import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('register/',user_views.register, name='register'),
    path('users/', include('django.contrib.auth.urls')),
    path('users/',include('users.urls')),

    path('test_pending', views.demo_pending, name='demo_Pending.html'),
    path('test_comp', TemplateView.as_view(template_name='demo_comp.html')),
    path('test_del', TemplateView.as_view(template_name='demo_del.html')),



    path('sales/', include('django.contrib.auth.urls')),
    path('sales/',include('sales.urls')),



    path('', views.dashboard, name='home'),
    #path('login/', LoginView.as_view(), name='login')

    
    #path('login/', LoginView.as_view(), name='login')
    path('sales/customer_reg/appointment_create.html', AppointmentCreateView.as_view(), name='apt-create'),
    path('appointments/update/<int:pk>/', AppointmentUpdateView.as_view(), name='apt-update'),
    path('appointments/cancel/<int:pk>/', AppointmentCancelView.as_view(), name='apt-cancel'),
    path("get_available_time_slots/", get_available_time_slots, name="get_available_time_slots"),


    # path('', TemplateView.as_view(template_name='dashboard.html'), name='home'),
    
    path('login/', LoginView.as_view(), name='login'),

   
    path('analytics', views.dashboard_with_pivot, name='dahsboard_with_pivot'),
    path('analytics_data', views.appointment_api, name='pivot_data'),
    path('chart', views.chart_test, name='chart'),
    path('chart_data', views.chart_weekly_appointments, name='chart_data'),
    path('line_data', views.chart_appointment_times, name='line_data'),


    path('appointment', views.appointment_api),
    path('appointment_pending', views.appointment_api_pending),
    path('appointment_Completed', views.appointment_api_Completed),
    path('appointment_Deleted', views.appointment_api_Deleted),
    path('search/', views.search_appointment_api, name = "search"),

    path('appointment', views.appointment_api)


]
