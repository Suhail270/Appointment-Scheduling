
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy, resolve
from .forms import AppointmentForm, customerform
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
    Status,
    Organization
)

def customer_reg(request, slug):
    organization = Organization.objects.get(choice=slug)

    if request.method == "POST":
        form = customerform(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            mobile = form.cleaned_data['mobile']
            email = form.cleaned_data['email']
            organization = form.cleaned_data['organization']

            user = User.objects.create(username=firstname, first_name=firstname, last_name=lastname, mobile=mobile, email=email, organization=organization)
            customer = Customer.objects.create(user=user, organization=organization)
            request.session['customer_id'] = customer.id

            return redirect("appointment_create.html")
    else:
        form = customerform(initial={'organization': organization})  # Set initial value for the hidden field

    return render(request, "custreg.html", {'form': form})

    # try:
    #     organization = Organization.objects.get(choice=slug) 

    # except Organization.DoesNotExist:
    #     organization = Organization.objects.create(choice=slug)

    # if request.method == "POST":
    #     form = NewUserForm(request.POST)
    #     if form.is_valid():
    #         user = form.save(commit=False)
    #         user.organization = organization
    #         user.save()
    #         agent = Agent.objects.create(user = user, organization = organization)
    #         login(request, user)
    #         messages.success(request, "Registration successful.")
    #     else:
    #         messages.error(request, "Unsuccessful registration. Invalid information.")
    # else:
    #     form = NewUserForm(initial={'organization': organization})  # Set initial value for the hidden field

    # return render(request=request, template_name="signup.html", context={"register_form": form})
  
class AppointmentCreateView(generic.CreateView):
    template_name = "sales/appointment_create.html"
    form_class = AppointmentForm

    def get_success_url(self):
        return reverse_lazy('home')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        return form

    def get_initial(self):
        initial = super().get_initial()

        # Retrieve the customer value from the session
        customer_id = self.request.session.get('customer_id')
        if customer_id:
            customer = Customer.objects.get(id=customer_id)
            initial['customer'] = customer

        # Retrieve the slug value from the URL
        slug = self.kwargs.get('slug')
        if slug:
            organization = Organization.objects.get(choice=slug)
            initial['organization'] = organization

        return initial

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

        customer_id = self.request.session.get('customer_id')

        if customer_id:
            customer = Customer.objects.get(id=customer_id)
            appointment.customer = customer

        appointment.customer = customer

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

        del self.request.session['customer_id']

        return super(AppointmentCreateView, self).form_valid(form)

    
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

class AppointmentUpdateView(generic.UpdateView):
    model = Appointment
    template_name = "sales/appointment_update.html"
    form_class = AppointmentForm

    def get_success_url(self):
        return reverse_lazy('home')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        return form

    def form_valid(self, form):
        appointment = form.save(commit=False)
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
        return super(AppointmentUpdateView, self).form_valid(form)


class AppointmentCancelView(generic.TemplateView):
    template_name = 'sales/appointment_cancel.html'
    
    def get(self, request, *args, **kwargs):

        appointment = Appointment.objects.get(id = int(request.path.split('/')[-2]))
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
        for appointment in existing_appointments:
            if appointment.status.choice != "Cancelled":  # Exclude cancelled appointments
                unavailable_slots.append(appointment.time.choice)

        all_time_slots = TimeChoices.objects.exclude(choice__in=unavailable_slots)
        available_time_slots = [{"id": time_slot.id, "choice": time_slot.choice} for time_slot in all_time_slots]

        return JsonResponse({"time_slots": available_time_slots})


