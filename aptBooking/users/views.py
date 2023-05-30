from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
#-----
from django.http import HttpResponse
#-----

# def register(request):
#     form = UserCreationForm()
#     template_name = 'signup.html'
#     return render(request, template_name,{'form':form})

def register(request):
    context ={}
    context['form']= UserCreationForm()
    return render(request, "users/register.html", context)

#-----
#request handler
def say_hello(request):
    return render(request,'users/hello.html', {'name' : 'Sally'})

def add(request):
    num1 = int (request.GET['num1'])
    num2 = int (request.GET['num2'])
    res = num1 + num2
    return render(request,'users/result.html', {'result': res})

#-----