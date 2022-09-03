from django.contrib import admin

# Register your models here.
from .models import Activity, Hotel, Rooms, Cost, Reservation, WaitLine

admin.site.register(Hotel)
admin.site.register(Rooms)
admin.site.register(Cost)
admin.site.register(Activity)
admin.site.register(Reservation)
admin.site.register(WaitLine)
