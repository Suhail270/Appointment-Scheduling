from django.shortcuts import render, redirect, reverse
from .forms import AppointmentForm
from django.views import generic
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from .models import (
    Customer,
    Agent,
    Appointment,
    TimeChoices,
    User
)

class AppointmentCreateView(generic.CreateView):
    template_name = "sales/appointment_create.html"
    form_class = AppointmentForm

    def get_success_url(self):
        return reverse("")
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        # form.fields['agent'].queryset = Agent.objects.filter(
        #     organization=user.userprofile
        # )
        return form

    def form_valid(self, form):
        appointment = form.save(commit=False)
        # appointment.organization = "Motors"
        selected_day = form.cleaned_data.get("day")
        selected_agent = form.cleaned_data.get("agent").user.email

         # Retrieve the unavailable time slots based on the selected day and agent
        existing_appointments = Appointment.objects.filter(day=selected_day, agent__user__email=selected_agent)
        unavailable_slots = [str(appointment.time) for appointment in existing_appointments]

         # Exclude the unavailable time slots from the available time slots
        available_time_slots = TimeChoices.objects.exclude(choice__in=unavailable_slots)

        # Save the form with the updated available time slots
        form.fields["time"].queryset = available_time_slots

        appointment.save()
        # send_mail(
        #     subject="An appointment has been created",
        #     message="SUCCESS",
        #     from_email="test@test.com",
        #     recipient_list=["test2@test.com"]
        # )
        # messages.success(self.request, "You have successfully created a lead")
        return super(AppointmentCreateView, self).form_valid(form)

def get_available_time_slots(request):
    if request.method == "GET":
        unavailable_slots = []
        available_time_slots = []
        selected_day = request.GET.get("day")
        selected_agent = Agent.objects.get(id=request.GET.get("agent"))

        existing_appointments = Appointment.objects.filter(day=selected_day, agent=selected_agent)
        unavailable_slots = [appointment.time.choice for appointment in existing_appointments]

        all_time_slots = TimeChoices.objects.exclude(choice__in=unavailable_slots)
        available_time_slots = [{"id": time_slot.id, "choice": time_slot.choice} for time_slot in all_time_slots]

        print("AVAILABLE: ", available_time_slots)

        return JsonResponse({"time_slots": available_time_slots})
