from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewUserForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sales.models import Appointment, Agent, User, Customer, Status, TimeChoices, PreferredContact,AgentCancelledAppointment
from sales.serializers import appointmentSerializer
from django.http.response import JsonResponse
from .tables import AppointmentTable
from django_tables2 import SingleTableView
from django.views.generic import ListView
#from django_filters.views import FilterView
#from django_filters import FilterSet
import simplejson
from django.core.mail import send_mail

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("dashboard.html")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="signup.html", context={"register_form":form})

# class AppointmentFilter(FilterSet):
#     Class Meta:
#         model = Appointment
#         fields -

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
        appointment = Appointment.objects.get(pk = int(request.POST.get('app_id')))
        appointment.status = Status.objects.get(pk = request.POST.get('app_stat'))
        appointment.save()
    stat_choices = [stat for stat in Status.objects.all()]
    return render(request=request, context={'choices': stat_choices}, template_name="update_appointment.html")

#fetching appointment based on APPOINTMENT ID
def delete_appointment_status(request):
    if request.method == 'POST':
        appointment_id = Appointment.objects.get(pk = int(request.POST.get('app_id')))
        reason_for_cancellation = request.POST.get('reason_for_cancel')
        status_id = Status.objects.filter(choice='Cancelled').values('id')[0]['id']  
        
        # print("---- status_id ---- ")
        # print(status_id)

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


def appointments(request):
    return render (request = request, template_name = "appointments.html")


@csrf_exempt
def appointment_api(request):
    if request.method == 'GET':
        agents = Agent.objects.all().select_related().filter(user_id = request.user.id)
        if len(agents) == 0:
            return JsonResponse(None, safe = False)
        appointments = Appointment.objects.all().filter(agent_id = int(agents[0].id))
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


# def send_email(request):
#     appointment_id = Appointment.objects.get(pk = int(request.POST.get('app_id')))
#     subject = request.POST.get('subject')
#     message = request.POST.get('message')
#     #message = f'Hi {user.username}, thank you for registering.'
#     email_from = appointment_id.agent.user.email
#     recipient_list = [appointment_id.customer.user.email, ]
#     send_mail( subject, message, email_from, recipient_list)
    