import operator
from django.shortcuts import render
from django.db.models import Q

from .forms import SearchFrom
from hotel.forms import ActivityForm
from hotel.models import Activity, Hotel, Rooms, Cost
from functools import reduce

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
        act = Activity.objects.filter(one_activity__in=checked_activities)
        hotel_ids = {}
        for item in act:
            id=item.hotel.id
            if id in hotel_ids:
                hotel_ids[id] = hotel_ids[id] + 1
            else:
                hotel_ids[id]=1
        for (_) in list(hotel_ids):
            if hotel_ids[_] != len(checked_activities):
                hotel_ids.pop(_)
        hotels = Hotel.objects.filter(city=city, id__in=hotel_ids)
    else:
        hotels = Hotel.objects.filter(city=city)

    rooms = Rooms.objects.filter(people=people, hotel__in = hotels)
    cost = Cost.objects.filter(begin_date__lte = start, end_date__gte = end,
        room__in=rooms).order_by('-cost')
    
    week_cost = []
    for _ in cost: 
        week_cost.append((end-start).days*_.cost)
        
    cost = zip(cost,week_cost)
    context = { 
        'costs' : cost,
        'form' : form,
        # 'stelle' : range(5),
        'activities' : activities,
        'checked_activities' : checked_activities,
    }
    return render(request, "search.html", context)