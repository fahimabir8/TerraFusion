from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lat = models.FloatField()  # Latitude of the selected location
    lon = models.FloatField()  # Longitude of the selected location
    selected_date = models.DateField()  # User's selected date for overpass
    created_at = models.DateTimeField(auto_now_add=True)  # When the selection was made
    

class UserLocation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

class SatellitePass(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    satellite_name = models.CharField(max_length=100)
    pass_time = models.DateTimeField()
    notification_sent = models.BooleanField(default=False)
    

class NotificationRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    bounding_box = models.JSONField()  # To store the coordinates of the bounding box
    notified = models.BooleanField(default=False)  # To track if the notification has been sent

    def __str__(self):
        return f"Notification for {self.user} on {self.date}"