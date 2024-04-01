from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from datetime import date

# Create your models here.
class Info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=50)


class Car(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField(blank=True, null=True)
    km = models.IntegerField(blank=True, null=True)
    color = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True, blank=True)
    doors = models.IntegerField(blank=True, null=True)
    photo = models.ImageField(null=True, default='car-icon.png')
    available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    price = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        current_date = date.today()
        reservations = Reservation.objects.filter(
            car=self,
            start__lte=current_date,
            end__gte=current_date,
            confirmed=True
        )

        if reservations.exists():
            self.available = False
        else:
            self.available = True
        super(Car, self).save(*args, **kwargs)

    class Meta():
        ordering = ['-updated', '-created']


class Reservation(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    confirmed = models.BooleanField(default=False)

    class Meta():
        ordering = ['-updated', '-created']


class Review(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    show = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)

    class Meta():
        ordering = ['-created']


class Logs(models.Model):
    type_choices = [('V', 'Voiture'), ('C', 'Client'), ('R', 'Reservation')]

    created = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=1, choices=type_choices)

    class Meta():
        ordering = ['-created']
