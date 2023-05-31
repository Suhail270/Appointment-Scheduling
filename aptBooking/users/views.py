from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewUserForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from sales.models import Appointment, Agent
from sales.serializers import appointmentSerializer, agentSerializer
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

def agent(request):
    return render (request = request, template_name = "agents.html")

@csrf_exempt
def appointment_api(request):
    if request.method == 'GET':
        a_id_list = Agent.objects.all().filter(user_id = request.user.id)
        if len(a_id_list) == 0:
            return JsonResponse(None, safe = False)
        a_id = int(a_id_list[0].id)
        appointments = Appointment.objects.all().filter(agent_id = a_id)
        serialized = appointmentSerializer(appointments, many = True)
        return JsonResponse(serialized.data, safe = False)
    

def agent_info(request):
    a_id_list = Agent.objects.all().filter(user_id = request.user.id)
    if len(a_id_list) == 0:
        return JsonResponse(None, safe = False)
    #a_id = int(a_id_list[0].id)
    serialized = agentSerializer(a_id_list, many = True)
    return JsonResponse(serialized.data, safe = False)
    