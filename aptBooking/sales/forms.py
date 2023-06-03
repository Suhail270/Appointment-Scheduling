from django import forms
from sales.models import TimeChoices,Agent,PreferredContact
import datetime
class customerform(forms.Form):
    firstname = forms.CharField(label='Enter Firstname:',max_length=100)
    lastname = forms.CharField(label='Enter lastname:',max_length=100)
    mobile = forms.CharField(label='Enter Mobile No:',max_length=30)
    email = forms.EmailField(label='Enter email:')

class DateInput(forms.DateInput):
    input_type = 'date'

class appointmentform(forms.Form):
    customerid = forms.IntegerField()
    # date = forms.DateField(initial=datetime.date.today)
    date = forms.DateField(widget = DateInput)
    time = forms.ModelChoiceField(queryset=TimeChoices.objects.all())
    agents = forms.ModelChoiceField(queryset=Agent.objects.all())
    contactpref = forms.ModelChoiceField(queryset=PreferredContact.objects.all())