from django.contrib import admin
from .models import Info, Car, Reservation, Logs, Review

# Register your models here.
admin.site.register(Info)
admin.site.register(Car)
admin.site.register(Reservation)
admin.site.register(Logs)
admin.site.register(Review)