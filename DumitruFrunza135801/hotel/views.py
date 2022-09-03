from calendar import week
from datetime import datetime
from functools import total_ordering
from pickletools import read_uint1
from turtle import begin_fill
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .forms import HotelForm, RoomsForm, CostForm
from django.forms import formset_factory, modelformset_factory
from .models import Hotel, Reservation, Rooms, Cost, Activity, WaitLine
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail
from .tasks import add
import re

def hotel_view(request,*args,**kwargs):
    return render(request,"registra_struttura.html",{})

def struttura(request, id):
    try:
        hotel = Hotel.objects.get(id = id)
    except Hotel.DoesNotExist:
        raise Http404
    form = HotelForm(request.POST or None, instance=hotel)

    if form.is_valid():
        activities_string = hotel.free_time
        activities_list = re.compile('\w+').findall(activities_string)
        for activity in activities_list:
            if not Activity.objects.filter(hotel=hotel, one_activity=activity):
                Activity.objects.create(hotel=hotel, one_activity=activity)
        form.save()
        return redirect('/hotel/list')
    context = {
        "form": form,
        "obj_id" : hotel.id
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

@login_required
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

@login_required
def reserve_room(request, cost_id, start, end):
    start_date = datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.strptime(end, '%Y-%m-%d').date()
    cost = Cost.objects.get(id=cost_id)
    week_cost = (end_date-start_date).days*cost.cost
    context = {
        'start' : start_date,
        'end' : end_date,
        'cost' : cost,
        'user' : request.user,
        'week_cost' : week_cost
    }
    if request.POST:
        cost = Cost.objects.get(id = request.POST['cost_id'])
        Reservation.objects.create(
            user = request.user,
            cost = cost,
            begin_date = start,
            end_date = end,
            total_cost = week_cost
        )
        return redirect('/my_reservations')
    return render(request, 'one_reservation.html', context)

@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    context={   
        'query' : reservations
    }
    return render(request, 'reservation_list.html', context)

@login_required
def delete_reservation(request, res_id):
    res = Reservation.objects.get(id = res_id)
    res.delete()
    return redirect('my_reservations')

@login_required
def update_reservation(request, res_id):
    res = Reservation.objects.get(id = res_id)
    raw_begin_date = str(res.begin_date)
    raw_end_date = str(res.end_date)
    if request.POST: 
        start = request.POST['start']
        end = request.POST['end']

        other_res = Reservation.objects.filter(
            end_date__gte = start,
            begin_date__lte = end
        ).exclude(id = res.id)

        check_av = Cost.objects.filter(begin_date__lte = start, 
            end_date__gte = end, room = res.cost.room)
    
        if check_av and not other_res:
            res.begin_date = start
            res.end_date = end
            res.save()
            return redirect('/my_reservations')
        else: 
            messages.error(request, 'Data non disponibile')
    context = { 
        'res' : res,
        'raw_begin_date' : raw_begin_date,
        'raw_end_date' : raw_end_date,
    }
    return render(request, 'edit_reservation.html', context)

@login_required
def wait_line(request, start, end, people, city):
    start_date = datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.strptime(end, '%Y-%m-%d').date()
    context = {
        'city' : city,
        'start' : start_date,
        'end' : end_date,
        'people' : people
    }
    start_date = datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.strptime(end, '%Y-%m-%d').date()
    if request.POST:
        print(city)
        print(request.POST)
        WaitLine.objects.create(
            user = request.user,
            begin_date = start_date,
            city = request.POST['city'],
            end_date = end_date,
            people = request.POST['people'],
        )

    return render(request, 'wait_line.html', context)
