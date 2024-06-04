import math
from geographiclib.geodesic import Geodesic
from geopy import distance
def calculate_sensor_dimensions(diagonal_inches, aspect_ratio):
    """
    Calculate the width and height of a camera sensor based on its diagonal size in inches and aspect ratio.
    The output dimensions are in millimeters.

    Parameters:
    diagonal_inches (float): The diagonal size of the sensor in inches.
    aspect_ratio (tuple): A tuple representing the aspect ratio (width, height).

    Returns:
    tuple: A tuple containing the width and height of the sensor in millimeters.
    """
    # Conversion factor from inches to millimeters
    mm_per_inch = 25.4

    # Convert diagonal from inches to millimeters
    diagonal_mm = diagonal_inches * mm_per_inch

    # Extract the width-to-height ratio from the aspect ratio tuple
    w_ratio, h_ratio = aspect_ratio

    # Convert aspect ratio to float
    aspect_ratio_float = w_ratio / h_ratio

    # Calculate width using the derived formula
    width = diagonal_mm / math.sqrt(1 + (1/aspect_ratio_float)**2)

    # Calculate height using the aspect ratio and width
    height = width / aspect_ratio_float

    return width, height

def calculate_gsd(sensor_dimension_x_mm, sensor_dimension_y_mm, altitude_m, sensor_resolution_x, sensor_resolution_y, focal_length_mm):
    """
    Calculate the Ground Sampling Distance (GSD) in meters.

    Parameters:
    sensor_dimension_mm (float): The size of the sensor dimension (width height) in mm.
    altitude_m (float): The altitude above the ground in meters.
    sensor_resolution (int): The number of pixels along the sensor dimension (width or height).
    focal_length_mm (float): The focal length of the camera in millimeters.

    Returns:
    float: The Ground Sampling Distance (GSD) in meters.
    """
    
    # Calculate GSD in millimeters using the formula
    gsd_x_m = (sensor_dimension_x_mm * altitude_m) / (sensor_resolution_x * focal_length_mm)
    gsd_y_m = (sensor_dimension_y_mm * altitude_m) / (sensor_resolution_y * focal_length_mm)

    return gsd_x_m, gsd_y_m

def calculate_offset(drone_lon, drone_lat, image_width_x, image_height_y, px_x, px_y, bearing, altitude_m, diagonal_size_inches, aspect_ratio, focal_length_mm):
    
    #invert yolo ref frame
    px_y = image_height_y - px_y

    #print("RUEDI", px_y)

    sensor_dimension_x_mm, sensor_dimension_y_mm = calculate_sensor_dimensions(diagonal_size_inches, aspect_ratio)
    
    gsd_x, gsd_y = calculate_gsd(sensor_dimension_x_mm, sensor_dimension_y_mm, altitude_m, image_width_x, image_height_y, focal_length_mm)

    # Calculate the offset in meters from the center of the image to the point
    center_x, center_y = image_width_x / 2, image_height_y / 2
    meters_offset_x = (px_x - center_x) * gsd_x
    meters_offset_y = (px_y - center_y) * gsd_y

    #print(meters_offset_x, meters_offset_y)
    #############
    ###NOT ACCURATE
    EARTH_RADIUS = 6371000  # Earth radius in meters
    
    # Convert bearing to radians
    bearing_radians = math.radians(bearing)
    
    # Rotate the delta offsets based on the bearing
    # Bearing is measured clockwise from north, thus use the standard rotation formula
    rotated_delta_x = meters_offset_x * math.cos(bearing_radians) + meters_offset_y * math.sin(bearing_radians)
    rotated_delta_y = -meters_offset_x * math.sin(bearing_radians) + meters_offset_y * math.cos(bearing_radians)
    #print(rotated_delta_x, rotated_delta_y)
    # Convert delta meters to radians
    delta_lat = rotated_delta_y / EARTH_RADIUS
    delta_lon = rotated_delta_x / (EARTH_RADIUS * math.cos(math.radians(drone_lat)))

    # Convert radians to degrees
    delta_lat_deg = math.degrees(delta_lat)
    delta_lon_deg = math.degrees(delta_lon)

    # Calculate new geographic coordinates
    new_latitude = drone_lat + delta_lat_deg
    new_longitude = drone_lon + delta_lon_deg
    ###NOT ACCURATE
    #########################
    distance, angle = cartesian_to_polar_north(rotated_delta_x,rotated_delta_y)
    geod = Geodesic.WGS84
    theta = angle #direction from North, clockwise 
    shift = distance #meters

    g = geod.Direct(drone_lat, drone_lon, angle, shift)

    lat2 = g['lat2']
    lon2 = g['lon2']

    #return new_longitude, new_latitude
    return lon2, lat2
    
def generate_google_maps_link(longitude, latitude):
    """
    Generate a link to Google Maps for the given longitude and latitude.

    Parameters:
    longitude (float): Longitude of the location.
    latitude (float): Latitude of the location.

    Returns:
    str: URL to Google Maps pointing to the specified location.
    """
    base_url = "https://www.google.com/maps/search/?api=1&query="
    return f"{base_url}{latitude},{longitude}"

def cartesian_to_polar_north(x, y):
    """
    Convert Cartesian coordinates (x, y) to polar coordinates (distance, degrees) with angle relative to North.

    :param x: x-coordinate (east-west displacement)
    :param y: y-coordinate (north-south displacement)
    :return: A tuple (distance, degrees) where:
             - distance is the radial distance from the origin
             - degrees is the angle in degrees from the north, measured clockwise
    """
    # Calculate the radial distance using the Pythagorean theorem
    distance = math.sqrt(x**2 + y**2)
    
    # Calculate the angle in radians from the north, then convert to degrees
    radians = math.atan2(x, y)
    degrees = math.degrees(radians)
    
    # Adjust the degrees to be between 0 and 360
    degrees = (degrees + 360) % 360
    
    return distance, degrees

if __name__ == "__main__":

    diagonal_size_inches = 1/1.3  # example diagonal in inches
    aspect_ratio = (4, 3)  # example aspect ratio
    altitude_m = 15        # Altitude in meters
    focal_length_mm = 24    # Focal length in millimeters
    drone_longitude = -20.249132
    drone_latitude = 63.445533
    image_width_x = 1920  # pixels
    image_height_y = 1080  # pixels
    px_x = 832.79596  # pixel x coordinate
    px_y = 52.755585  # pixel y coordinate
    bearing = 180 # Bearing in degrees

   
    sensor_dimension_x_mm, sensor_dimension_y_mm = calculate_sensor_dimensions(diagonal_size_inches, aspect_ratio)
    print(sensor_dimension_x_mm, sensor_dimension_y_mm)

    gsd_x, gsd_y = calculate_gsd(sensor_dimension_x_mm, sensor_dimension_y_mm, altitude_m, image_width_x, image_height_y, focal_length_mm)
    print(gsd_x, gsd_y)

    new_lon, new_lat = calculate_offset(drone_longitude, drone_latitude, image_width_x, image_height_y, px_x, px_y, bearing, altitude_m, diagonal_size_inches, aspect_ratio, focal_length_mm)

    print(f"The geographic coordinates of the drone are Longitude: {drone_longitude}, Latitude: {drone_latitude}")
    print(f"The geographic coordinates of the point are Longitude: {new_lon}, Latitude: {new_lat}")
   
    orig = ( drone_latitude, drone_longitude)
    objcord = ( new_lat,new_lon)

    print(distance.distance(objcord,orig).meters)

    #link = generate_google_maps_link(drone_longitude, drone_latitude)

    #print("Google Maps Link:", link)

    #link = generate_google_maps_link(new_lon, new_lat)
    #print("Google Maps Link:", link)
