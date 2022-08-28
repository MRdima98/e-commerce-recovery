from calendar import firstweekday
from email import message
from multiprocessing import context
from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib import messages

def log_in(request):
    return render(request, 'log_in.html', {})

def register(request):
    register_form = RegisterForm(request.POST or None)
    if register_form.is_valid():
        if register_form.cleaned_data['passwd'] == register_form.cleaned_data['confirm_passwd']:
            User.objects.create_user(
                username = register_form.cleaned_data['username'],
                first_name = register_form.cleaned_data['name'],
                last_name = register_form.cleaned_data['surname'],
                email = register_form.cleaned_data['email'],
                password = register_form.cleaned_data['passwd'],
            )
        else: 
            print('nope')
            messages.error(request, 'Le password non coincidono')
    
    context = { 'form' : register_form }
    return render(request, 'register.html', context)

def log_or_register(request):
    return render(request, 'log_or_register.html', {})