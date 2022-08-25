from django.shortcuts import render, redirect
from django.http import Http404

from .forms import HotelForm, RoomsForm, CostForm
from django.forms import formset_factory, modelformset_factory
from .models import Hotel, Rooms, Cost, Activity
import re

def hotel_view(request,*args,**kwargs):
    return render(request,"registra_struttura.html",{})

def struttura(request, id):
    try:
        obj = Hotel.objects.get(id = id)
    except Hotel.DoesNotExist:
        raise Http404
    form = HotelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/hotel/list')
    context = {
        "form": form,
        "obj_id" : obj.id
    }
    return render(request, "registra_struttura.html", context)

def hotel_list(request):
    obj = Hotel.objects.all()
    context = { "objects": obj }
    return render(request, "hotel_list.html", context)

def delete_hotel(request, id):
    hotel = Hotel.objects.get(id=id)
    hotel.delete()
    return redirect('/hotel/list')

def new_hotel(request):
    my_form = HotelForm(request.POST or None)
    if my_form.is_valid():
        hotel = Hotel.objects.create(**my_form.cleaned_data)
        activities_string = hotel.free_time
        activities_list = re.compile('\w+').findall(activities_string)
        for activity in activities_list:
            Activity.objects.create(hotel=hotel, one_activity=activity)
        return redirect('/hotel/rooms/' + str(hotel.id) + '&1')
    context = { "form" : my_form }
    return render(request, 'registra_struttura.html', context )

def add_edit_room(request, hotel_id, room_id):
    rooms_form = RoomsForm(request.POST or None, request.FILES or None)
    cost_factory = formset_factory(CostForm, extra = 4)
    cost_formset = cost_factory(request.POST or None)
    hotel = Hotel.objects.get(id=hotel_id)
    if cost_formset.is_valid() and rooms_form.is_valid():
        room = Rooms.objects.create(**rooms_form.cleaned_data, hotel = hotel)
        for cost_form in cost_formset:
            if cost_form.is_valid():
                Cost.objects.create(**cost_form.cleaned_data, room = room)
        if room_id == hotel.rooms_count:
            return redirect('/hotel/list')
        return redirect('/hotel/rooms/' + str(hotel_id) + '&' + str(room_id+1))
    context = { 'rooms_form' : rooms_form, 'cost_form' : cost_formset }
    return render(request, 'one_room.html', context)

def room_list(request, hotel_id):
    hotel = Hotel.objects.get(id = hotel_id)
    obj = Rooms.objects.filter(hotel = hotel)
    context = { 
        "obj": obj,
        "rooms_count": range(int(hotel.rooms_count)) ,
        "hotel_id" : hotel.id 
        }
    return render(request, "room_list.html", context)

def edit_room(request, room_id, hotel_id):
    try:
        room = Rooms.objects.get(id = room_id)
    except Hotel.DoesNotExist:
        raise Http404
    rooms_form = RoomsForm(request.POST or None, instance = room)
    cost_factory = modelformset_factory(Cost, form = CostForm, extra = 0)
    query = Cost.objects.filter(room=room)
    cost_ids = Cost.objects.filter(room=room).values_list('id', flat=True)
    cost_formset = cost_factory(request.POST or None, queryset = query)
    if rooms_form.is_valid() and cost_formset.is_valid():
        rooms_form.save()
        for form in cost_formset:
            if form.is_valid():
                if form.cleaned_data['id'] == None:
                    Cost.objects.create(**form.cleaned_data, room = room)
                else:
                    form.save()
        return redirect('/hotel/rooms/' + str(hotel_id))
                
    context = {
        "rooms_form" : rooms_form, 
        "cost_form" : cost_formset,
        "cost_ids" : cost_ids,
    }

    return render(request, 'one_room.html', context)