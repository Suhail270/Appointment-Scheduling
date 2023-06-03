from django import forms

from .models import TimeChoices,Agent,PreferredContact
import datetime
class customerform(forms.Form):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    mobile = forms.CharField(max_length=30)
    email = forms.EmailField()


class DateInput(forms.DateInput):
    input_type = 'date'


class appointmentform(forms.Form):
    # date = forms.DateField(initial=datetime.date.today)
    date = forms.DateField(widget = DateInput)
    time = forms.ModelChoiceField(queryset=TimeChoices.objects.all())
    agents = forms.ModelChoiceField(queryset=Agent.objects.all())
    contactpref = forms.ModelChoiceField(queryset=PreferredContact.objects.all())

