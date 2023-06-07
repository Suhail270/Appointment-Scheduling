from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewUserForm ,DateForm 
from django.contrib.auth import login
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sales.models import Appointment, Agent, User, Customer, Status, TimeChoices, PreferredContact,AgentCancelledAppointment, Organization
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
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.forms.models import model_to_dict

def register(request, slug):
    # Retrieve the organization instance based on the slug or segment
    try:
        organization = Organization.objects.get(choice=slug) 

    except Organization.DoesNotExist:
        organization = Organization.objects.create(choice=slug)

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.organization = organization
            user.save()
            agent = Agent.objects.create(user = user, organization = organization)
            return login(request, user)
            messages.success(request, "Registration successful.")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm(initial={'organization': organization})  # Set initial value for the hidden field

    return render(request=request, template_name="signup.html", context={"register_form": form})


# def dateTime(request):
#     context={}
#     context['context']=DateForm()
#     return render(request=request, template_name="dashboard.html",context={"context":context})

# class AppointmentFilter(FilterSet):
#     Class Meta:
#         model = Appointment
#         fields -
#check victor

# class appointmentsListView(SingleTableView):
#     model = Appointment
#     table_class = AppointmentTable
#     template_name = 'appointments.html'

#     def get_queryset(self, *args, **kwargs):
#         qs = super(appointmentsListView, self).get_queryset(*args, **kwargs)
#         a_id_list = Agent.objects.all().filter(user_id = self.request.user.id)
#         a_id = int(a_id_list[0].id)
#         qs = qs.all().filter(agent_id = a_id)
#         return qs

# @csrf_exempt
# def update_appointment_status(request):
#     if request.method == 'POST':
#         print(request.POST)
#         appointment = Appointment.objects.get(pk = int(request.POST.get('app_id')))
#         appointment.status = Status.objects.get(pk = request.POST.get('app_stat'))
#         appointment.save()
#     stat_choices = [stat for stat in Status.objects.all()]
#     return render(request=request, context={'choices': stat_choices}, template_name="update_appointment.html")

# @csrf_exempt
# def dashboard_dropdown(request):
#     if request.method == 'POST':
#         appointment = Appointment.objects.get(pk = int(request.POST.get('app_id')))
#         appointment.status = Status.objects.get(pk = request.POST.get('app_stat'))
#         appointment.save()
#     if True:
#         stat_choices = [stat for stat in Status.objects.all()]
#         return render(request=request, context={'choices': stat_choices}, template_name="dashboard.html")

@csrf_exempt
def dashboard(request):
    
    if request.method == 'POST':
        appointment = Appointment.objects.get(pk = int(request.POST.get('app_id')))
        appointment.status = Status.objects.get(choice = request.POST.get('app_stat'))
        appointment.save()

    stat_choices = [stat for stat in Status.objects.all()]
    return render(request=request, context={'choices': stat_choices}, template_name="dashboard.html")

# def update_appointment_status_completed(request):
#     if request.method == 'POST':
#         appointment = Appointment.objects.get(pk = int(request.POST.get('app_id')))
#         appointment.status = Status.objects.get(choice = request.POST.get('app_stat'))
#         appointment.save()
#     stat_choices = [stat for stat in Status.objects.all()]
#     return render(request=request, context={'choices': stat_choices}, template_name="update_appointment.html")

@csrf_exempt
def search_appointment_api(request):
       
        user = request.user
                
        if user.is_organizer is True:
            
            agents = Agent.objects.all().filter(organization = user.organization)
            #if date or time is Null, display all appointments
            if (date is None):
                appointments = Appointment.objects.all().filter(organization = user.organization)
            #if not, display appointments of given date and time    
            else:
                appointments = Appointment.objects.all().filter(day = date, time_id = time_slot, organization = user.organization)

        else:
            
            agents = Agent.objects.all().select_related().filter(user_id = user.id)
            #if date or time is Null, display all appointments
            if (date is None):
                appointments = Appointment.objects.all().filter(agent_id = int(agents[0].id))
            #if not, display appointments of given date and time    
            else:
                appointments = Appointment.objects.all().filter(agent_id = int(agents[0].id), day = date, time_id = time_slot)
        
        if len(agents) == 0:
                return JsonResponse(None, safe = False)

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
                    'agent': str(appointment.agent.user.first_name) + " " + str(appointment.agent.user.last_name),
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
    
    user = request.user

    if request.method == 'GET':
        
        if user.is_organizer is True:
            agents = Agent.objects.all().filter(organization = user.organization)
            appointments = Appointment.objects.all().filter(organization = user.organization)
             
        else:
            agents = Agent.objects.all().select_related().filter(user_id = user.id)
            appointments = Appointment.objects.all().filter(agent_id = int(agents[0].id))

        if len(agents) == 0:
            return JsonResponse(None, safe = False)
        
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
            appointment_dict['agent'] = str(appointment.agent.user.first_name) + " " + str(appointment.agent.user.last_name)
            appointment_dict['status'] = str(appointment.status.choice)
            appointments_data.append(appointment_dict)

        return JsonResponse(appointments_data, safe=False)

def appointment_api_pending(request):
    user = request.user
   
    if request.method == 'GET':
        
        if user.is_organizer is True:
            agents = Agent.objects.all().filter(organization = user.organization)
            appointments = Appointment.objects.all().filter(organization = user.organization).filter(status = Status.objects.get(choice = 'Pending'))
        else:
            agents = Agent.objects.all().select_related().filter(user_id = user.id)
            appointments = Appointment.objects.all().filter(agent_id = int(agents[0].id)).filter(status = Status.objects.get(choice = 'Pending'))

        if len(agents) == 0:
            return JsonResponse(None, safe = False)

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
                    'agent': str(appointment.agent.user.first_name) + " " + str(appointment.agent.user.last_name),
                    'status': str(appointment.status.choice)
                } for appointment in appointments
            ]
        )
        # serialized = appointmentSerializer(appointments, many = True)
        return JsonResponse(simplejson.loads(json), safe = False)

# my part

def appointment_api_Completed(request):
    user = request.user
    if request.method == 'GET':

        if user.is_organizer is True:
            agents = Agent.objects.all().filter(organization = user.organization)
            appointments = Appointment.objects.all().filter(organization = user.organization).filter(status = Status.objects.get(choice = 'Completed'))
        else:
            agents = Agent.objects.all().select_related().filter(user_id = user.id)
            appointments = Appointment.objects.all().filter(agent_id = int(agents[0].id)).filter(status = Status.objects.get(choice = 'Completed'))

        if len(agents) == 0:
            return JsonResponse(None, safe = False)

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
                    'agent': str(appointment.agent.user.first_name) + " " + str(appointment.agent.user.last_name),
                    'status': str(appointment.status.choice)
                } for appointment in appointments
            ]
        )
        # serialized = appointmentSerializer(appointments, many = True)
        return JsonResponse(simplejson.loads(json), safe = False)

#my part

def appointment_api_Deleted(request):
    user = request.user
    if request.method == 'GET':
        if user.is_organizer is True:
            agents = Agent.objects.all().filter(organization = user.organization)
            appointments = Appointment.objects.all().filter(organization = user.organization).filter(status = Status.objects.get(choice = 'Cancelled'))
        else:
            agents = Agent.objects.all().select_related().filter(user_id = user.id)
            appointments = Appointment.objects.all().filter(agent_id = int(agents[0].id)).filter(status = Status.objects.get(choice = 'Cancelled'))

        if len(agents) == 0:
            return JsonResponse(None, safe = False)
        
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
                    'agent': str(appointment.agent.user.first_name) + " " + str(appointment.agent.user.last_name),
                    'status': str(appointment.status.choice)
                } for appointment in appointments
            ]
        )
        # serialized = appointmentSerializer(appointments, many = True)
        return JsonResponse(simplejson.loads(json), safe = False)


# currently shows form for email subject and body to agent, need to be autogenereated

#fetching appointment based on APPOINTMENT ID
def delete_appointment_status(request):
    
    user = request.user

    if request.method == 'POST':
        
        appointment_id = Appointment.objects.get(pk = int(request.POST.get('app_id')))
        print("APPOINTMENT: ", appointment_id)
        reason_for_cancellation = request.POST.get('reason_for_cancel')
        status_id = Status.objects.filter(choice='Cancelled').values('id')[0]['id']  
        
        print("---- appointment_id ---- ")
        print(request.POST.get('app_id'))
        print("APPOINTMENT: ", appointment_id)

        #updating status of appointment to cancelled
        appointment_id.status = Status.objects.get(pk = status_id)
        appointment_id.save()

        if user.is_organizer:
            organization = user.organization
        
        else:
            agent = Agent.objects.all().select_related().filter(user_id = user.id)
            organization = agent.organization

        #adding appointment to cancelled appointments table
        
        # organization = Organization.objects.get(choice=slug) 
        new_record = AgentCancelledAppointment(appointment = appointment_id, reason = reason_for_cancellation, organization = organization)
        new_record.save()

        #sending an email
        
        customer = str(Appointment.objects.get(pk = int(request.POST.get('app_id'))).customer.user.first_name)
        agent = Appointment.objects.get(pk = int(request.POST.get('app_id'))).agent

        subject = "Appointment Cancellation"
        message = '''Dear ''' + customer + ''',
        
We are sorry to inform you that your appointment with agent ''' + str(agent.user.first_name) + " " + str(agent.user.last_name) + " on " + str(appointment_id.day) + " at " + str(appointment_id.time.choice) + ''' has been cancelled.
        
Please book another appointment with us via our portal or contact our customer support for more information. We apologize for any inconvenience caused and are contantly working to improve our customer experience.
        
We hope to you see you soon!'''

        email_from = appointment_id.agent.user.email
        recipient_list = [appointment_id.customer.user.email,]
        send_mail(subject, message, email_from, recipient_list)

        return redirect('home') 
    
    return render(request=request, template_name="delete_appointment.html")

