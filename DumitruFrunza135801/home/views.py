from django.shortcuts import render
from .froms import SearchFrom
# Create your views here.

from hotel.models import Hotel

def home(request, *args, **kwargs):
    form = SearchFrom()
    if request.method == "GET": 
        form = SearchFrom(request.GET)
        if form.is_valid():
            return search(request, form.cleaned_data.get('city'))
    context = {
        "form" : form
    }
    return render(request, "index.html", context)

def search(request, city):
    result = Hotel.objects.filter(city = city) 
    context = {
        "result" : result
    }
    return render(request, "search.html", context)