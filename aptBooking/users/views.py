from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewUserForm
from django.contrib.auth import login

def  register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("dashboard.html")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="signup.html", context={"register_form":form})


#-----
#request handler
def say_hello(request):
    return render(request,'users/hello.html', {'name' : 'Sally'})

def add(request):
    num1 = int (request.POST['num1'])
    num2 = int (request.POST['num2'])
    res = num1 + num2
    return render(request,'users/result.html', {'result': res})

#-----
