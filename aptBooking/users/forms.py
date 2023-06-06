from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField ,UserCreationForm
from django.forms.widgets import DateInput
# Create your forms here.
from django.utils import timezone
from sales.models import TimeChoices 

User = get_user_model()

# class AgentModelForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = (
#             'email',
#             'username',
#             'first_name',
#             'last_name'
#         )

class NewUserForm(UserCreationForm):
    # organization = forms.CharField(widgets=forms.HiddenInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'mobile', 'organization')
        field_classes = {"username": UsernameField}

 

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

class DateInput(forms.DateInput):
	input_type='date'

class DateForm(forms.Form):
	day = forms.DateField(
        widget=RestrictedDateInput(),
        help_text="Please select a date within 30 days from today."
    )