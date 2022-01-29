from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Alarm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="alarms")
    name = models.CharField(max_length=32)
    time = models.TimeField()
    medname = models.CharField(max_length=64)
    status = models.CharField(max_length=10, default='Not taken', blank=True, null=True)
    REPEAT = models.BooleanField(default=False, blank=True, null=True)
    repeat_time = models.TimeField(default=None, blank=True, null=True)
    turned_on = models.CharField(max_length=2, default='On', blank=True, null=True)

    def __str__(self):
        return f"Alarm '{self.name}' at {self.time}"