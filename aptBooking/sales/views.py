from django.shortcuts import render
from .forms import NewCustForm, NewApptForm


# Create your views here.
def custreg(request):
    context ={}
    context['custform']= NewCustForm()
    return render(request, "custreg.html", context)

def appt(request):
    context ={}
    context['apptform']= NewApptForm()
    return render(request, "appt.html", context)

