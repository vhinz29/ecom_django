from django.db import models
import datetime
from django.contrib.auth.models import User



class Logo(models.Model):
    logo = models.ImageField(upload_to='uploads/pictures/', blank=True, null=True)
    name_logo = models.CharField(max_length=150, blank=True, null=True )

    def __str__(self):
        return self.name_logo


class Zone(models.Model):
    name_zone = models.CharField(max_length=50)

    def __str__(self):
        return self.name_zone

class Todaname(models.Model):
    name_toda = models.CharField(max_length=50 ,blank=True, null=True)
    brgy_name = models.CharField(max_length=100 ,blank=True, null=True)
    todazone = models.ForeignKey(Zone, on_delete=models.CASCADE ,default=1)

    def __str__(self):
        return self.name_toda


class Profile(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE ,default=1)
    user = models.OneToOneField(User, on_delete=models.CASCADE ,default=1)
    todaname = models.ForeignKey(Todaname, on_delete=models.CASCADE, default=1)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE ,default=1)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    bodynum = models.CharField(max_length=20 ,blank=True, null=True)
    license_id = models.CharField(max_length=20, blank=True, null=True)
    license_expired = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='uploads/pictures/' )
    # is_seen = models.BooleanField('is_seen',default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Notifies(models.Model):
    notify_user = models.CharField(max_length=30,blank=True, null=True)
    is_seen = models.BooleanField('is_seen',default=False)

    def __str__(self):
        return self.notify_user

    class Meta:
        verbose_name_plural = 'Notifies'

