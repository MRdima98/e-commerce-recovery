from multiprocessing import context
from django.shortcuts import render
from .forms import RegisterForm

def log_in(request):
    return render(request, 'log_in.html', {})

def register(request):
    register_form = RegisterForm(request.POST or None)
    if register_form.is_valid():
        pass
    context = { 'form' : register_form }
    return render(request, 'register.html', context)

def log_or_register(request):
    return render(request, 'log_or_register.html', {})