from django.shortcuts import render
from .forms import RegisterForm, LogInForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect

def log_in(request):
    log_in_form = LogInForm(request.POST or None)
    if log_in_form.is_valid():
        user = authenticate(
            username = log_in_form.cleaned_data['username'],
            password = log_in_form.cleaned_data['passwd']
        )
        if user is not None:
            login(request, user)
            next = request.GET.get('next', '/')
            return HttpResponseRedirect(next)
        else:
            print('NO')
    context = { 'form' : log_in_form }
    return render(request, 'log_in.html', context)

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
            messages.error(request, 'Le password non coincidono')
    
    context = { 'form' : register_form }
    return render(request, 'register.html', context)

def my_logout(request):
    logout(request)
    next = request.GET.get('next', '/')
    return HttpResponseRedirect(next)

def go_back(request):
    next = request.GET.get('next', '/')
    return HttpResponseRedirect(next)
