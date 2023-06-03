from django.shortcuts import render,redirect
from .forms import customerform, appointmentform
from sales.models import Appointment, Agent, User, Customer, Status, TimeChoices, PreferredContact
# Create your views here.

def customer_reg(request):
    if (request.method == "POST"):
        form = customerform(request.POST)
        if (form.is_valid()):
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            mobile = form.cleaned_data['mobile']
            email = form.cleaned_data['email']
            user = User.objects.create(username=firstname,first_name = firstname,last_name = lastname, mobile = mobile, email = email)
            user.save()
            customer = Customer.objects.create(user = user)
            return redirect("appointment.html")
    form = customerform()
    return render(request,"customer.html",{'form': form})

def appointment(request):
    if (request.method == "POST"):
        form = appointmentform(request.POST)
        if (form.is_valid()):
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            agent = form.cleaned_data['agents']
            contactpref = form.cleaned_data['contactpref']
            customerid = form.cleaned_data['customerid']
            customer = Customer.objects.get(user_id = customerid)
            appointment = Appointment.objects.create(customer = customer, day = date, agent = agent, time = time, preferred_contact_method = contactpref)
            appointment.save()
    form = appointmentform()
    return render(request,"appointment.html",{'form': form})

def success(request):
    return render(request,"success.html")