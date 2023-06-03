from django import forms
from .models import TimeChoices, Customer

# Create your forms here.

class NewCustForm(forms.Form):
    first_name = forms.CharField(max_length = 200)
    last_name = forms.CharField(max_length = 200)
    email_address = forms.EmailField(max_length = 200)
    mobile_number = forms.CharField()

    # class Meta:
    #     model = Customer
    #     field = ['name', 'email', 'mobile']

class DateInput(forms.DateInput):
    input_type = 'date'

class NewApptForm(forms.Form):
    date = forms.DateField(widget = DateInput)
    time = forms.ModelChoiceField(queryset=TimeChoices.objects.all())