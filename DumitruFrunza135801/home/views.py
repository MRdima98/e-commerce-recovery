from django.shortcuts import render
from .froms import SearchFrom
# Create your views here.

from hotel.models import Hotel, Rooms

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
    hotel = Hotel.objects.filter(city = city) 
    rooms = Rooms.objects.filter(hotel = hotel[0])
    print(hotel)
    context = {
        'rooms' : rooms,
        'results' : range(len(hotel)),
        'hotel' : hotel 
    }
    return render(request, "search.html", context)