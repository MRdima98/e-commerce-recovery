from django.contrib import admin

# Register your models here.
from .models import Hotel, Rooms, Cost

admin.site.register(Hotel)
admin.site.register(Rooms)
admin.site.register(Cost)