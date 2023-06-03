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