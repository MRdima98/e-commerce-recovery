from django.shortcuts import render
from django.forms import formset_factory, modelformset_factory

from .forms import SearchFrom
from hotel.forms import ActivityForm
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
    activities = Activity.objects.all().values('one_activity').distinct()
    checked_activities = request.GET.getlist('activities')
    if checked_activities:
        hotels = Hotel.objects.filter(city=city, 
        activity__one_activity__in=checked_activities)
    else:
        hotels = Hotel.objects.filter(city=city)
    rooms = Rooms.objects.filter(people=people, hotel__in = hotels)
    cost = Cost.objects.filter(begin_date__lte = start, end_date__gte=end,
        room__in=rooms)
    
    print(request.GET.getlist('activities'))
    context = { 
        'costs' : cost,
        'form' : form,
        'stelle' : range(5),
        'activities' : activities,
        'checked_activities' : checked_activities,
    }
    return render(request, "search.html", context)