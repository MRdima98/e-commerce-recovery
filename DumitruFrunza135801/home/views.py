import datetime
from random import choices
from threading import local
from django.shortcuts import render

from hotel.forms import ActivityForm
from .forms import SearchFrom
# Create your views here.

from hotel.models import Activity, Hotel, Rooms, Cost

def home(request):
    form = SearchFrom()
    if request.method == "GET": 
        form = SearchFrom(request.GET)
        if form.is_valid():
            data = form.cleaned_data
            return search(request, data.get('city'), data.get('start'),
                data.get('end'), data.get('how_many')
            )
    context = {
        "form" : form
    }
    return render(request, "index.html", context)

def search(request, city, start, end, people):
    form = SearchFrom(
        initial= {
            'city' : city,
            'start' : start,
            'end' : end,
            'how_many' : people
        }
    )
    hotels = Hotel.objects.filter(city=city)
    rooms = Rooms.objects.filter(people=people, hotel__in = hotels)
    cost = Cost.objects.filter(begin_date__lte = start, end_date__gte=end,
        room__in=rooms)
    activities = Activity.objects.filter(hotel__in=hotels).values(
        'one_activity').distinct()
    activities_form = ActivityForm(data=activities.values)

    print(activities)
    context = { 
        'costs' : cost,
        'form' : form,
        'stelle' : range(5),
        'activities' : activities,
        'activities_form' : activities_form
    }
    return render(request, "search.html", context)