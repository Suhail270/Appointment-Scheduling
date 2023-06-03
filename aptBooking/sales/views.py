from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy, resolve
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
    User,
    Status
)

class AppointmentCreateView(generic.CreateView):
    template_name = "sales/appointment_create.html"
    form_class = AppointmentForm

    def get_success_url(self):
        return reverse_lazy('home')
    
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
        update_url = reverse("apt-update", kwargs={"pk": appointment.pk})
        cancel_url = reverse("apt-cancel", kwargs={"pk": appointment.pk})
        send_mail(
            subject="An appointment has been created",
            message="Feel free to update at: " + update_url + " and feel free to cancel at: " + cancel_url,
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        messages.success(
            self.request,
            f"You have successfully created an appointment. You can update the details <a href='{update_url}'>here</a>."
        )
        return super(AppointmentCreateView, self).form_valid(form)
    
class AppointmentUpdateView(generic.UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'sales/appointment_update.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, "Appointment details have been updated.")
        return super().form_valid(form)

class AppointmentCancelView(generic.TemplateView):
    template_name = 'sales/appointment_cancel.html'
    
    def get(self, request, *args, **kwargs):
        
        appointment = Appointment.objects.get(id = request.path[-2])
        appointment.status = Status.objects.get(id = 2)
        appointment.save()
        
        return super().get(request, *args, **kwargs)


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
