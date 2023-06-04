from django import forms

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Appointment, TimeChoices, User, Agent, PreferredContact
import datetime

from django.forms.widgets import DateInput
from django.utils import timezone
from django.utils.safestring import mark_safe

User = get_user_model()

class customerform(forms.Form):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    mobile = forms.CharField(max_length=30)
    email = forms.EmailField()

class DateInput(forms.DateInput):
    input_type = 'date'

from django.forms.widgets import DateInput
from django.utils import timezone

class RestrictedDateInput(DateInput):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        today = timezone.localdate()
        max_date = today + timezone.timedelta(days=30)
        context['widget']['attrs']['max'] = max_date.isoformat()
        context['widget']['attrs']['min'] = today.isoformat()
        return context

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs['autocomplete'] = 'off'
        attrs['readonly'] = 'readonly'
        return attrs


class AppointmentForm(forms.ModelForm):
    day = forms.DateField(
        widget=RestrictedDateInput(),
        help_text="Please select a date within 30 days from today."
    )

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

    def clean_day(self):
        day = self.cleaned_data.get('day')

        # Check if the selected day is in the past
        if day < timezone.localdate():
            raise forms.ValidationError("Please select a date from today or the future.")

        # Check if the selected day is more than 30 days in the future
        max_allowed_date = timezone.localdate() + timezone.timedelta(days=30)
        if day > max_allowed_date:
            raise forms.ValidationError("Please select a date within 30 days from today.")

        return day

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize other field attributes or widgets if needed

