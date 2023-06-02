from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.forms import UsernameField ,UserCreationForm

# Create your forms here.

class NewUserForm(UserCreationForm):

	class Meta:
		model = User
		fields = ('username','email','mobile')
		field_classes = {"username":UsernameField} 

