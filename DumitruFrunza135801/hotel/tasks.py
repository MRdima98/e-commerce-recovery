from celery import shared_task
from django.core.mail import send_mail
from .models import Cost, Reservation, Hotel, Rooms, WaitLine

@shared_task
def add():
    line = WaitLine.objects.all()
    
    for user in line: 
        hotels = Hotel.objects.filter(city=user.city)

        rooms = Rooms.objects.filter(people=user.people, hotel__in = hotels)
        reservations = Reservation.objects.filter(
            end_date__gte = user.begin_date,
            begin_date__lte = user.end_date
        )

        cost_ids = []
        for id in reservations:
            cost_ids.append(id.cost.id)

        cost = Cost.objects.filter(
            begin_date__lte = user.begin_date, 
            end_date__gte = user.end_date,
            room__in=rooms
        ).order_by('-cost').exclude(id__in = cost_ids)
        if cost:
            send_mail(
                'Disponibili',
                'Abbiamo nuovi risultati',
                'dimafrunza69@gmail.com',
                ['mrdima88@yahoo.it'],
                fail_silently=False,
            )