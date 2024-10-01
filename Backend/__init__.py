import geopandas as gpd
from shapely.geometry import Point

# Load the WRS-2 shapefile (make sure the path is correct and includes the .shp extension)
wrs_shapefile = "D:/ProjectLandsat/Backend/WRS2_descending.shp"
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

# Example: Coordinates for a location (latitude and longitude)
latitude = 24.479
longitude = 90.607

# Call the function to find the Path/Row for this location
path, row = latlon_to_pathrow(latitude, longitude)

# Output the results
if path and row:
    print(f"Path: {path}, Row: {row}")
else:
    print("No matching Path/Row found for this location.")
