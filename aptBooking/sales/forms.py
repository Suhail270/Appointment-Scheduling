from django import forms

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Appointment, TimeChoices, User, Agent, PreferredContact
import datetime

User = get_user_model()

class customerform(forms.Form):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    mobile = forms.CharField(max_length=30)
    email = forms.EmailField()

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

# class appointmentform(forms.Form):
#     # date = forms.DateField(initial=datetime.date.today)
#     date = forms.DateField(widget = DateInput)
#     time = forms.ModelChoiceField(queryset=TimeChoices.objects.all())
#     agents = forms.ModelChoiceField(queryset=Agent.objects.all())
#     contactpref = forms.ModelChoiceField(queryset=PreferredContact.objects.all())
    
class DateInput(forms.DateInput):
    input_type = 'date
