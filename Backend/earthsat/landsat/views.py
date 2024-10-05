# from django.shortcuts import render
# from django.http import JsonResponse
# import geopandas as gpd
# from shapely.geometry import Point
# from django.views.decorators.csrf import csrf_exempt
# import json

# Load the WRS-2 shapefile (make sure the path is correct and includes the .shp extension)
# wrs_shapefile =  "D:/TerraFusion/Backend/Notification/WRS2_descending.shp"
# # "D:/ProjectLandsat/Backend/WRS2_descending.shp"
# wrs = gpd.read_file(wrs_shapefile)

# # Create a function to check if a latitude/longitude point is within the bounding box of any polygon
# def latlon_to_pathrow(lat, lon):
#     # Create a Point from the longitude (x) and latitude (y)
#     point = Point(lon, lat)
    
#     # Iterate through each row in the GeoDataFrame
#     for index, row in wrs.iterrows():
#         polygon = row['geometry']  # Get the polygon geometry
        
#         # Get the bounding box of the polygon (returns a tuple (minx, miny, maxx, maxy))
#         minx, miny, maxx, maxy = polygon.bounds
        
#         # Check if the point is inside the bounding box
#         if minx <= lon <= maxx and miny <= lat <= maxy:
#             return row['PATH'], row['ROW']  # Return the Path/Row if point is within the bounding box
    
#     return None, None  # Return None if no matching bounding box is found


# # Django view to handle incoming coordinates
# @csrf_exempt
# def get_path_row(request):
#     if request.method == 'POST':
#         try:
#             # Parse the request body as JSON
#             data = json.loads(request.body)
#             latitude = data.get('latitude')
#             longitude = data.get('longitude')
            
#             if latitude and longitude:
#                 # Example logic to compute path/row based on lat/lon
#                 path = 123  # Example value
#                 row = 456   # Example value
#                 return JsonResponse({'path': path, 'row': row})
#             else:
#                 return JsonResponse({'error': 'Invalid coordinates'}, status=400)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json  # Import the json module
from datetime import datetime, timedelta
from django.shortcuts import render
from .models import UserLocation,NotificationRequest
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



# NASA Earthdata API Token
TOKEN = 'eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6ImZhaGltX2FiaXIiLCJleHAiOjE3MzMwNDU3MDgsImlhdCI6MTcyNzg2MTcwOCwiaXNzIjoiaHR0cHM6Ly91cnMuZWFydGhkYXRhLm5hc2EuZ292In0.OK15F-GoDBr2BKeqcNGm-DfidEqivn8S6vGVhWPhXKCjQtEudNMp7oHBHabDg7l5Dg9vFahsDcmlf_1eU5nGpSeXC416m4-Iz-l_YVPvRC00mQT4RUuitrWG_9pETRQZ8u15e0PlAIGNeGn6nabusJT_RZMc5QPNCwKjuMROfu7gVJQ1Gul5D6maiXt35Fja9HTZ5ggrUpt4UVjmQ2ex8VEHHiqoj6GuxwKF3KQzTWhyv-zkcqhwzV8L21XzqfoBqlNVEj1XDmfebNaSBgHfETWKecjGRiQ5BDvtaqJ_8p0CdjGSgA7FBc9ZJkMyy3nj930xnIC6z9u7TNCLOhCoPg'

@csrf_exempt  # Disable CSRF just for testing, remember to handle this properly in production
def get_data(request):
    if request.method == 'POST':
        # Parse the incoming JSON request
        data = json.loads(request.body)
        bounding_box = data.get('bounding_box')
        selected_date = data.get('date')

        # Ensure bounding box and date are provided
        if not bounding_box or len(bounding_box) != 4 or not selected_date:
            return JsonResponse({'error': 'Invalid bounding box or date'}, status=400)

        # Convert the date into a temporal range (e.g., ±3 days)
        selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
        start_date = (selected_date_obj - timedelta(days=3)).strftime('%Y-%m-%dT00:00:00Z')
        end_date = (selected_date_obj + timedelta(days=3)).strftime('%Y-%m-%dT23:59:59Z')

        # Construct the bounding box string in the format required by the NASA API
        bbox_str = f'{bounding_box[1]},{bounding_box[0]},{bounding_box[3]},{bounding_box[2]}'

        # NASA Earthdata API URL
        url = 'https://cmr.earthdata.nasa.gov/search/granules.json'
        params = {
            'collection_concept_id': 'C2021957657-LPCLOUD',  # Replace with your collection ID
            'temporal': f'{start_date},{end_date}',  # Temporal range
            'bounding_box': bbox_str
        }

        headers = {
            'Authorization': f'Bearer {TOKEN}'
        }

        # Send request to NASA Earthdata API
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            # Parse the response and extract relevant data
            data = response.json()
            granules = data.get('feed', {}).get('entry', [])

            if granules:
                results = []
                for granule in granules:
                    results.append({
                        'title': granule['title'],
                        'href': granule['links'][0]['href']  # Assume the first link is the download link
                    })

                return JsonResponse({'results': results})
            else:
                return JsonResponse({'results': []})  # No data found

        return JsonResponse({'error': 'No data found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def home(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        user_location, created = UserLocation.objects.update_or_create(
            user=request.user,
            defaults={'latitude': latitude, 'longitude': longitude}
        )
    return render(request, 'index.html')


def notify_user(user_id, message):
    # Debugging: Print to check when a notification is sent
    print(f"Sending notification to user {user_id}: {message}")

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'user_{user_id}',
        {
            'type': 'send_notification',
            'message': message,
        }
    )

@csrf_exempt
def request_notification(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User not authenticated."}, status=403)

        data = json.loads(request.body)
        bounding_box = data.get('bounding_box')
        date = data.get('date')

        # Create a NotificationRequest for the user
        notification_request = NotificationRequest.objects.create(
            user=request.user,  # Assuming the user is authenticated
            date=date,
            bounding_box=bounding_box
        )

        return JsonResponse({"message": "Notification request received."}, status=200)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=400)
