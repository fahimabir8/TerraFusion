from django.shortcuts import render
from django.http import JsonResponse
import geopandas as gpd
from shapely.geometry import Point
from django.views.decorators.csrf import csrf_exempt
import json

# Load the WRS-2 shapefile (make sure the path is correct and includes the .shp extension)
wrs_shapefile =  "D:/TerraFusion/Backend/Notification/WRS2_descending.shp"
# "D:/ProjectLandsat/Backend/WRS2_descending.shp"
wrs = gpd.read_file(wrs_shapefile)

# Create a function to check if a latitude/longitude point is within the bounding box of any polygon
def latlon_to_pathrow(lat, lon):
    # Create a Point from the longitude (x) and latitude (y)
    point = Point(lon, lat)
    
    # Iterate through each row in the GeoDataFrame
    for index, row in wrs.iterrows():
        polygon = row['geometry']  # Get the polygon geometry
        
        # Get the bounding box of the polygon (returns a tuple (minx, miny, maxx, maxy))
        minx, miny, maxx, maxy = polygon.bounds
        
        # Check if the point is inside the bounding box
        if minx <= lon <= maxx and miny <= lat <= maxy:
            return row['PATH'], row['ROW']  # Return the Path/Row if point is within the bounding box
    
    return None, None  # Return None if no matching bounding box is found


# Django view to handle incoming coordinates
@csrf_exempt
def get_path_row(request):
    if request.method == 'POST':
        try:
            # Parse the request body as JSON
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            
            if latitude and longitude:
                # Example logic to compute path/row based on lat/lon
                path = 123  # Example value
                row = 456   # Example value
                return JsonResponse({'path': path, 'row': row})
            else:
                return JsonResponse({'error': 'Invalid coordinates'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)