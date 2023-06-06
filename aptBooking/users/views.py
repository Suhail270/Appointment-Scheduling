from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewUserForm ,DateForm 
from django.contrib.auth import login
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sales.models import Appointment, Agent, User, Customer, Status, TimeChoices, PreferredContact,AgentCancelledAppointment
from sales.serializers import appointmentSerializer
from django.http.response import JsonResponse
from .tables import AppointmentTable
from django_tables2 import SingleTableView
from django.views.generic import ListView
from django_filters.views import FilterView
from django_filters import FilterSet
import simplejson
from django.views.decorators.csrf import csrf_exempt
import time

import datetime

from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
import math


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="signup.html", context={"register_form":form})

def dateTime(request):
    context={}
    context['context']=DateForm()
    return render(request=request, template_name="dashboard.html",context={"context":context})

# class AppointmentFilter(FilterSet):
#     Class Meta:
#         model = Appointment
#         fields -
#check victor
class appointmentsListView(SingleTableView):
    model = Appointment
    table_class = AppointmentTable
    template_name = 'appointments.html'

    def get_queryset(self, *args, **kwargs):
        qs = super(appointmentsListView, self).get_queryset(*args, **kwargs)
        a_id_list = Agent.objects.all().filter(user_id = self.request.user.id)
        a_id = int(a_id_list[0].id)
        qs = qs.all().filter(agent_id = a_id)
        return qs


def update_appointment_status(request):
    if request.method == 'POST':
        print(request.POST)
        appointment = Appointment.objects.get(pk = int(request.POST.get('app_id')))
        appointment.status = Status.objects.get(pk = request.POST.get('app_stat'))
        appointment.save()
    stat_choices = [stat for stat in Status.objects.all()]
    return render(request=request, context={'choices': stat_choices}, template_name="update_appointment.html")

@csrf_exempt
def dashboard_dropdown(request):
    if request.method == 'POST':
        appointment = Appointment.objects.get(pk = int(request.POST.get('app_id')))
        appointment.status = Status.objects.get(pk = request.POST.get('app_stat'))
        appointment.save()
    if True:
        stat_choices = [stat for stat in Status.objects.all()]
        number = Appointment.objects.filter(agent = Agent.objects.get(user_id = request.user.id)).count()
        return render(request=request, context={'choices': stat_choices}, template_name="dashboard.html")



@csrf_exempt
def dashboard(request):
    if request.method == 'POST':
        print(request.POST)
        appointment = Appointment.objects.get(pk = int(request.POST.get('app_id')))
        appointment.status = Status.objects.get(choice = request.POST.get('app_stat'))
        appointment.save()
    if True:
        stat_choices = [stat for stat in Status.objects.all()]
        number =( Appointment.objects.filter(agent = Agent.objects.get(user_id = request.user.id)).count())/2
        number=math.ceil(number)
        number = [i + 1 for i in range(number)]
    if request.GET == {}:
        return render(request=request, context={'choices': stat_choices,'number':number, 'thepage': 1}, template_name="dashboard.html")
    else:
        return render(request=request, context={'choices': stat_choices,'number':number, 'thepage': int(request.GET.getlist('page_id')[0])}, template_name="dashboard.html")

def dashboard_with_pivot(request):
    return render(request, 'dashboard_with_pivot.html', {})

# def pivot_data(request):
#     dataset = Order.objects.all()
#     data = serializers.serialize('json', dataset)
#     return JsonResponse(data, safe=False)

def update_appointment_status_completed(request):
    if request.method == 'POST':
        appointment = Appointment.objects.get(pk = int(request.POST.get('app_id')))
        appointment.status = Status.objects.get(choice = request.POST.get('app_stat'))
        appointment.save()
    stat_choices = [stat for stat in Status.objects.all()]
    return render(request=request, context={'choices': stat_choices}, template_name="update_appointment.html")

@csrf_exempt
def search_appointment_api(request):
        agents = Agent.objects.all().select_related().filter(user_id = request.user.id)
        if len(agents) == 0:
            return JsonResponse(None, safe = False)
        
        #if date or time is Null, display all appointments
        if (date is None):
            appointments = Appointment.objects.all().filter(agent_id = int(agents[0].id))

        #if not, display appointments of given date and time    
        else:
            appointments = Appointment.objects.all().filter(agent_id = int(agents[0].id), day = date, time_id = time_slot)

        # 'customer': str(users.filter(id = customers.filter(id = appointment.customer_id)[0].user_id)[0].username)
        # 'customer_first_name': str(appointment.customer.user.first_name),
        #             'customer_last_name': str(appointment.customer.user.last_name),
        json = simplejson.dumps(
            [
                {
                    'id': str(appointment.id),
                    'customer': str(appointment.customer.user.username),
                    'email': str(appointment.customer.user.email),
                    'mobile': str(appointment.customer.user.mobile),
                    'day': str(appointment.day),
                    'time': str(appointment.time.choice),
                    'preferred_contact_method': str(appointment.preferred_contact_method.choice),
                    'status': str(appointment.status.choice)
                } for appointment in appointments
            ]
        )
        # serialized = appointmentSerializer(appointments, many = True)
        return JsonResponse(simplejson.loads(json), safe = False)


@csrf_exempt
def search_demo(request):
    global date
    global time_slot
    date = request.POST.get('date')
    print("-----------------------")
    time_slot = request.POST.get('time')
    print(date)
    print(time_slot)

    time_choices = [stat for stat in TimeChoices.objects.all()]
    return render(request = request, context={'choices': time_choices}, template_name = "search_demo.html")


@csrf_exempt
def appointment_api(request):
    if request.method == 'GET':
        agents = Agent.objects.all().select_related().filter(user_id = request.user.id)
        if len(agents) == 0:
            return JsonResponse(None, safe = False)
        appointments = Appointment.objects.all().filter(agent_id = int(agents[0].id))
        paginator = Paginator(appointments, per_page=2)  
        page_number = request.GET.get('page')  
        customers = Customer.objects.all()
        users = User.objects.all()

        # 'customer': str(users.filter(id = customers.filter(id = appointment.customer_id)[0].user_id)[0].username)
        # 'customer_first_name': str(appointment.customer.user.first_name),
        #             'customer_last_name': str(appointment.customer.user.last_name),
        # json = simplejson.dumps(
        #     [
        #         {
        #             'id': str(appointment.id),
        #             'customer': str(appointment.customer.user.username),
        #             'email': str(appointment.customer.user.email),
        #             'mobile': str(appointment.customer.user.mobile),
        #             'day': str(appointment.day),
        #             'time': str(appointment.time.choice),
        #             'preferred_contact_method': str(appointment.preferred_contact_method.choice),
        #             'status': str(appointment.status.choice)
        #         } for appointment in appointments
        #     ]
        # )
        # # serialized = appointmentSerializer(appointments, many = True)
        # return JsonResponse(simplejson.loads(json), safe = False)
        try:
            appointments_page = paginator.get_page(page_number)
        except:
            return JsonResponse({'error': 'Invalid page number'}, status=400)

        appointments_data = []
        for appointment in appointments_page:
            appointment_dict = model_to_dict(appointment)
            appointment_dict['customer'] = str(appointment.customer.user.username)
            appointment_dict['email'] = str(appointment.customer.user.email)
            appointment_dict['mobile'] = str(appointment.customer.user.mobile)
            appointment_dict['time'] = str(appointment.time.choice)
            appointment_dict['preferred_contact_method'] = str(appointment.preferred_contact_method.choice)
            appointment_dict['status'] = str(appointment.status.choice)
            appointments_data.append(appointment_dict)

        return JsonResponse(appointments_data, safe=False)
    
def appointments(request):
    return render (request = request, template_name = "appointments.html")


def appointment_api_pending(request):
    if request.method == 'GET':
        agents = Agent.objects.all().select_related().filter(user_id = request.user.id)
        if len(agents) == 0:
            return JsonResponse(None, safe = False)
        appointments = Appointment.objects.all().filter(agent_id = int(agents[0].id)).filter(status = Status.objects.get(choice = 'Pending'))
        customers = Customer.objects.all()
        users = User.objects.all()

        # 'customer': str(users.filter(id = customers.filter(id = appointment.customer_id)[0].user_id)[0].username)
        # 'customer_first_name': str(appointment.customer.user.first_name),
        #             'customer_last_name': str(appointment.customer.user.last_name),
        json = simplejson.dumps(
            [
                {
                    'id': str(appointment.id),
                    'customer': str(appointment.customer.user.username),
                    'email': str(appointment.customer.user.email),
                    'mobile': str(appointment.customer.user.mobile),
                    'day': str(appointment.day),
                    'time': str(appointment.time.choice),
                    'preferred_contact_method': str(appointment.preferred_contact_method.choice),
                    'status': str(appointment.status.choice)
                } for appointment in appointments
            ]
        )
        # serialized = appointmentSerializer(appointments, many = True)
        return JsonResponse(simplejson.loads(json), safe = False)

# @csrf_exempt
# def appointment_pivot_api(request):
#     if request.method == 'GET':
#         agents = Agent.objects.all().select_related().filter(user_id = request.user.id)
#         if len(agents) == 0:
#             return JsonResponse(None, safe = False)
#         appointments = Appointment.objects.all().filter(agent_id = int(agents[0].id))
#         customers = Customer.objects.all()
#         users = User.objects.all()
#         dates = []
#         for i in range(30):
#             date = datetime.date.today() - datetime.timedelta(days = i)
#             dates.append(date)

#         # 'customer': str(users.filter(id = customers.filter(id = appointment.customer_id)[0].user_id)[0].username)
#         # 'customer_first_name': str(appointment.customer.user.first_name),
#         #             'customer_last_name': str(appointment.customer.user.last_name),
#         result = []
#         for date in dates:
#             date_appointments = appointments.filter(day = date)
#             if len(date_appointments) == 0:
#                 result.append(
#                     {
#                         'id': None,
#                         'customer': None,
#                         'email': None,
#                         'mobile': None,
#                         'day': date,
#                         'time': None,
#                         'preferred_contact_method': None,
#                         'status': None
#                     }
#                 )
#             for appointment in date_appointments:
#                 result.append(appointment)
#         json = simplejson.dumps(
#             [
#                 {
#                     'id': str(appointment.id),
#                     'customer': str(appointment.customer.user.username),
#                     'email': str(appointment.customer.user.email),
#                     'mobile': str(appointment.customer.user.mobile),
#                     'day': str(appointment.day),
#                     'time': str(appointment.time.choice),
#                     'preferred_contact_method': str(appointment.preferred_contact_method.choice),
#                     'status': str(appointment.status.choice)
#                 } for appointment in appointments
#             ]
#         )
        
        # serialized = appointmentSerializer(appointments, many = True)
        # return JsonResponse(simplejson.loads(json), safe = False)

def chart_test(request):
    return render(request, "charts_new.html", {})

def chart_appointment_times(request):
    no_of_days = int(request.GET.getlist('days')[0])
    agents = Agent.objects.all().select_related().filter(user_id = request.user.id)
    appointments = Appointment.objects.all().filter(agent_id = int(agents[0].id))
    times = TimeChoices.objects.all()
    date = datetime.date.today() - datetime.timedelta(no_of_days)
    times_list = [t.choice for t in times]
    time_appointments_completed = [0 for t in times]
    time_appointments_cancelled = [0 for t in times]
    date_appointments = appointments.filter(day__gt=date)
    print('here')
    for i in range(len(times_list)):
        time_appointments_completed[i] = date_appointments.filter(time = times[i]).filter(status = Status.objects.get(choice = "Completed")).count()
        time_appointments_cancelled[i] = date_appointments.filter(time = times[i]).filter(status = Status.objects.get(choice = "Cancelled")).count()
    line_data = {
        "labels": times_list,
        "completed_apps": time_appointments_completed,
        "cancelled_apps": time_appointments_cancelled, 
    }
    print(line_data)
    return JsonResponse(line_data, safe=False)
        

def chart_weekly_appointments(request):
    no_of_days = int(request.GET.getlist('days')[0])
    dates = []
    completed = []
    cancelled = []
    agents = Agent.objects.all().select_related().filter(user_id = request.user.id)
    appointments = Appointment.objects.all().filter(agent_id = int(agents[0].id))
    comp_stat = Status.objects.get(choice = "Completed")
    canc_stat = Status.objects.get(choice = "Cancelled")
    for i in range(no_of_days):
        date = datetime.date.today() - datetime.timedelta(days = i)
        dates.append(date)
        date_appointments = appointments.filter(day = date)
        completed.append(date_appointments.filter(status = comp_stat).count())
        cancelled.append(date_appointments.filter(status = canc_stat).count())
    bar_data = {
        "labels":dates[::-1],
        "chartLabel": "Completed",
        "chartdata":completed[::-1],
        "chartLabel2": "Cancelled",
        "chartdata2":cancelled[::-1],
    }
    return JsonResponse(bar_data, safe=False)
    
    


def chart_data(request):
    authentication_classes = []
    permission_classes = []
    labels = [
        'January',
        'February', 
        'March', 
        'April', 
        'May', 
        'June', 
        'July'
        ]
    chartLabel = "my data"
    chartdata = [0, 10, 5, 2, 20, 30, 45]
    data ={
                    "labels":labels,
                    "chartLabel":chartLabel,
                    "chartdata":chartdata,
            }
    print("@@@@@@@@@@@@")
    print(data)
    print("@@@@@@@@@@@@")
    return JsonResponse(data, safe=False)

def appointment_api_Completed(request):
    if request.method == 'GET':
        agents = Agent.objects.all().select_related().filter(user_id = request.user.id)
        if len(agents) == 0:
            return JsonResponse(None, safe = False)
        appointments = Appointment.objects.all().filter(agent_id = int(agents[0].id)).filter(status = Status.objects.get(choice = 'Completed'))
        customers = Customer.objects.all()
        users = User.objects.all()

        # 'customer': str(users.filter(id = customers.filter(id = appointment.customer_id)[0].user_id)[0].username)
        # 'customer_first_name': str(appointment.customer.user.first_name),
        #             'customer_last_name': str(appointment.customer.user.last_name),
        json = simplejson.dumps(
            [
                {
                    'id': str(appointment.id),
                    'customer': str(appointment.customer.user.username),
                    'email': str(appointment.customer.user.email),
                    'mobile': str(appointment.customer.user.mobile),
                    'day': str(appointment.day),
                    'time': str(appointment.time.choice),
                    'preferred_contact_method': str(appointment.preferred_contact_method.choice),
                    'status': str(appointment.status.choice)
                } for appointment in appointments
            ]
        )
        # serialized = appointmentSerializer(appointments, many = True)
        return JsonResponse(simplejson.loads(json), safe = False)

def appointment_api_Deleted(request):
    if request.method == 'GET':
        agents = Agent.objects.all().select_related().filter(user_id = request.user.id)
        if len(agents) == 0:
            return JsonResponse(None, safe = False)
        appointments = Appointment.objects.all().filter(agent_id = int(agents[0].id)).filter(status = Status.objects.get(choice = 'Cancelled'))
        customers = Customer.objects.all()
        users = User.objects.all()

        # 'customer': str(users.filter(id = customers.filter(id = appointment.customer_id)[0].user_id)[0].username)
        # 'customer_first_name': str(appointment.customer.user.first_name),
        #             'customer_last_name': str(appointment.customer.user.last_name),
        json = simplejson.dumps(
            [
                {
                    'id': str(appointment.id),
                    'customer': str(appointment.customer.user.username),
                    'email': str(appointment.customer.user.email),
                    'mobile': str(appointment.customer.user.mobile),
                    'day': str(appointment.day),
                    'time': str(appointment.time.choice),
                    'preferred_contact_method': str(appointment.preferred_contact_method.choice),
                    'status': str(appointment.status.choice)
                } for appointment in appointments
            ]
        )
        # serialized = appointmentSerializer(appointments, many = True)
        return JsonResponse(simplejson.loads(json), safe = False)



#fetching appointment based on APPOINTMENT ID
def delete_appointment_status(request):
    if request.method == 'POST':
        
        appointment_id = Appointment.objects.get(pk = int(request.POST.get('app_id')))
        reason_for_cancellation = request.POST.get('reason_for_cancel')
        status_id = Status.objects.filter(choice='Cancelled').values('id')[0]['id']  
        
        print("---- appointment_id ---- ")
        print(request.POST.get('app_id') == "")

        #updating status of appointment to cancelled
        appointment_id.status = Status.objects.get(pk = status_id)
        appointment_id.save()

        #adding appointment to cancelled appointments table
        new_record = AgentCancelledAppointment(appointment= appointment_id, reason= reason_for_cancellation)
        new_record.save()

        #sending an email
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email_from = appointment_id.agent.user.email
        recipient_list = [appointment_id.customer.user.email, ]
        send_mail(subject, message, email_from, recipient_list)

    return render(request=request, template_name="delete_appointment.html")


