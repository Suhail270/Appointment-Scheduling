from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewUserForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sales.models import Appointment, Agent
from sales.serializers import appointmentSerializer
from django.http.response import JsonResponse

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

def appointments(request):
    return render (request = request, template_name = "appointments.html")

@csrf_exempt
def appointment_api(request):
    if request.method == 'GET':
        a_id = int(Agent.objects.all().filter(user_id = request.user.id)[0].id)
        print(a_id)
        appointments = Appointment.objects.all().filter(agent_id = a_id)
        serialized = appointmentSerializer(appointments, many = True)
        return JsonResponse(serialized.data, safe = False)