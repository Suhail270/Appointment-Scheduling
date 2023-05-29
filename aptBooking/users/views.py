from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def register(request):
    form = UserCreationForm()
    template_name = 'signup.html'
    return render(request, template_name,{'form':form})
