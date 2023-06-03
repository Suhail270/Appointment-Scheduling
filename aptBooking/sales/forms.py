from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Appointment, TimeChoices, User, Agent

User = get_user_model()


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = (
            'customer',
            'agent',
            'day',
            'time',
            'preferred_contact_method',
            'status'
        )
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['time'].queryset = TimeChoices.objects.none()

        # if 'user' in self.data and len(Agent.objects.filter(organization='agent'.userprofile))==0:
        #     User.objects.create(name = 'name', organization = 'agent'.organization)
        # if 'day' in self.data:
        #     day = self.data['day']
        #     available_time_choices = self.get_available_time_choices(day)
        #     self.fields['time'].queryset = available_time_choices

    # def get_available_time_choices(self, day):
    #     existing_appointments = Appointment.objects.filter(day=day)
    #     all_time_choices = TimeChoices.objects.all()
    #     print("HI: \n")
    #     print(all_time_choices)
        # available_time_choices = all_time_choices.exclude(appointment__in=existing_appointments)
        # available_time_choices = all_time_choices
        # return available_time_choices

    # def clean_first_name(self):
    #     data = self.cleaned_data["first_name"]
    #     return data

    # def clean(self):
    #     pass