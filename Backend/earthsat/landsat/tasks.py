# from celery import shared_task
# from skyfield.api import Topos, load
# from django.utils.timezone import make_aware
# from datetime import datetime, timedelta
# from .models import UserLocation, SatellitePass
# from django.core.mail import send_mail

# @shared_task
# def check_satellite_passes():
#     # Load TLE data
#     stations_url = 'https://celestrak.com/NORAD/elements/resource.txt'
#     satellites = load.tle_file(stations_url)
#     landsat = {sat.name: sat for sat in satellites}.get('LANDSAT 8')

#     if not landsat:
#         return

#     ts = load.timescale()
#     start_time = datetime.utcnow()
#     end_time = start_time + timedelta(days=1)  # Check for the next 24 hours
#     start = ts.utc(start_time.year, start_time.month, start_time.day)
#     end = ts.utc(end_time.year, end_time.month, end_time.day)

#     # Iterate through users
#     for user_location in UserLocation.objects.all():
#         location = Topos(user_location.latitude, user_location.longitude)
#         t, events = landsat.find_events(location, start, end, altitude_degrees=10.0)

#         for ti, event in zip(t, events):
#             pass_time = make_aware(ti.utc_datetime())
#             SatellitePass.objects.create(
#                 user=user_location.user,
#                 satellite_name="LANDSAT 8",
#                 pass_time=pass_time,
#                 notification_sent=False
#             )
#             send_notification(user_location.user.email, pass_time)

# def send_notification(email, pass_time):
#     subject = f"LANDSAT 8 is passing over your location!"
#     message = f"Landsat 8 will be visible on {pass_time}. Don't miss it!"
#     send_mail(subject, message, 'from@example.com', [email])

from celery import shared_task
from .models import User
from .consumers import NotificationConsumer  # Your notify function

@shared_task
def check_landsat_passes():
    # Logic to check for new Landsat passes for each user
    for user in User.objects.all():
        # Example notification
        NotificationConsumer(user.id, "Landsat pass is approaching your location!")
