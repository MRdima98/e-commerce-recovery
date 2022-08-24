from django.shortcuts import render
from .froms import SearchFrom
# Create your views here.

from hotel.models import Hotel, Rooms, Cost

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
    hotels = Hotel.objects.filter(city = city) 
    for hotel in hotels:
        rooms = Rooms.objects.filter(hotel = hotel, 
        people=people).select_related('hotel')
    for room in rooms: 
        cost = Cost.objects.filter(room=room, begin_date=start, end_date=end).select_related('room')

    print(room,cost,hotels)
    context = {
        'rooms' : rooms,
        'results' : range(len(hotels)),
        'hotel' : hotels,
        'costs' : cost
    }
    return render(request, "search.html", context)