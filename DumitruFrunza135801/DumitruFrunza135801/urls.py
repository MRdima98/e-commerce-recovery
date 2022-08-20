"""DumitruFrunza135801 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from hotel.views import new_hotel, struttura, hotel_list, delete_hotel
from hotel.views import add_edit_room, room_list, edit_room
from home.views import home, search

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path('search/<str:city>',search, name='search'),

    path('hotel/', new_hotel, name='struttura'),
    path('struttura/<int:id>/', struttura),
    path('hotel/list', hotel_list, name="hotel_list"),
    path('hotel/delete/<int:id>', delete_hotel, name='delete'),
    path('hotel/rooms/<int:hotel_id>&<int:room_id>', add_edit_room, 
        name='add_edit_room'),
    path('hotel/rooms/<int:hotel_id>', room_list, name='room_list'),
    path('hotel/rooms/edit/<int:hotel_id>&<int:room_id>',
        edit_room, name='edit_room'),
]
