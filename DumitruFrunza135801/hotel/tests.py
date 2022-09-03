import json
from django.test import TestCase

# Create your tests here.

from .models import Reservation, Hotel, Cost, Rooms
from django.contrib.auth.models import User

class Tests(TestCase):
    def setUp(self):
        user = User.objects.create(
            username = 'username',
            password = 'password',
            first_name = 'name',
            last_name = 'surname',
            email = 'username@gmail.com',
        )
        self.hotel = Hotel.objects.create(
            name = 'hotel',
            IVA = '123456789012345',
            street = 'giradini 59',
            stars = 3,
            rooms_count = 1, 
            free_time = 'freesby',
            CAP = 41124,
            city = 'Modena',
            description = 'lorem'
        )
        room = Rooms.objects.create(
            hotel = self.hotel,
            name = 'room',
            people = '1',
            size = 25,
            description = 'lorem',
            photo = '/home/dima/e-commerce-recovery/DumitruFrunza135801/static/image/home-page-2.jpg',
        )
        cost = Cost.objects.create(
            room = room,
            cost = 5,
            begin_date = '2022-09-15',
            end_date = '2022-09-12',
        )
        self.one_reservation = Reservation.objects.create(
            user = user,
            cost = cost,
            begin_date = '2022-09-15',
            end_date = '2022-09-12',
            total_cost = 50,
        )

    def test_home_page(self):
        """Home page loads correctly"""
        response = self.client.get('http://localhost:8000')
        self.assertEquals(response.status_code, 200)

    def test_my_res(self):
        """Reservation is created correctly"""
        self.assertTrue(isinstance(self.one_reservation, Reservation))
