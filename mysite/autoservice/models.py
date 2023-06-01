from django.db import models
from django.contrib.auth.models import User
import datetime
import pytz
from tinymce.models import HTMLField
from PIL import Image

utc = pytz.UTC


class Service(models.Model):
    name = models.CharField('Pavadinimas', max_length=50)
    price = models.IntegerField('Kaina')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Paslauga"
        verbose_name_plural = "Paslaugos"


class VehicleModel(models.Model):
    make = models.CharField('Gamintojas', max_length=50)
    model = models.CharField('Modelis', max_length=50)

    def __str__(self):
        return f'{self.make} {self.model}'

    class Meta:
        verbose_name = "Automobilio modelis"
        verbose_name_plural = "Automobiliu modeliai"


class Vehicle(models.Model):
    plate = models.CharField('Valstybinis numeris', max_length=6)
    vin = models.CharField('VIN kodas', max_length=17)
    owner_name = models.CharField('Savininkas', max_length=50)
    photo = models.ImageField('Nuotrauka', upload_to='vehicles', null=True, blank=True)
    vehicle_model = models.ForeignKey(to='VehicleModel', verbose_name='Automobilio modelis', on_delete=models.SET_NULL,
                                      null=True)
    description = HTMLField('Aprasymas', null=True, blank=True)

    def __str__(self):
        return f'{self.vehicle_model} |{self.plate}|'

    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"


class Order(models.Model):
    date = models.DateTimeField(verbose_name='Data', auto_now_add=True)
    vehicle = models.ForeignKey(to='Vehicle', verbose_name='Automobilis', on_delete=models.SET_NULL, null=True)
    deadline = models.DateTimeField(verbose_name='Terminas', null=True, blank=True)
    client = models.ForeignKey(to=User, verbose_name='Klientas', on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('p', 'Patvirtinta'),
        ('v', 'Vykdoma'),
        ('a', 'Atsaukta'),
        ('t', 'Tvirtinama'),
        ('i', 'Ivykdita'),
    )

    status = models.CharField(verbose_name='Busena', max_length=1, choices=LOAN_STATUS, blank=True, default='t')

    def deadline_overdue(self):
        return self.deadline and datetime.datetime.today().replace(tzinfo=utc) > self.deadline.replace(tzinfo=utc)

    def total(self):
        total_sum = 0
        for line in self.lines.all():
            total_sum += line.sum()
        return total_sum

    def __str__(self):
        return f'{self.vehicle} ({self.date})'

    class Meta:
        verbose_name = "Uzsakymas"
        verbose_name_plural = "Uzsakymai"
        ordering = ['-id']


class OrderLine(models.Model):
    order = models.ForeignKey(to='Order', on_delete=models.CASCADE, related_name='lines')
    service = models.ForeignKey(to='Service', verbose_name='Paslauga', on_delete=models.SET_NULL, null=True)
    qty = models.IntegerField(verbose_name='Kiekis')

    def sum(self):
        return self.service.price * self.qty

    def __str__(self):
        return f'{self.order.vehicle} ({self.order.date}): {self.service} - {self.qty}'

    class Meta:
        verbose_name = "Uzsakymo eilute"
        verbose_name_plural = "Uzsakymu eilutes"


class OrderComment(models.Model):
    order = models.ForeignKey(to="Order", on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(to=User, verbose_name="Autorius", on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    content = models.TextField(verbose_name='Tekstas', max_length=5000)

    class Meta:
        verbose_name = "Komentaras"
        verbose_name_plural = 'Komentarai'
        ordering = ['-date_created']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)
