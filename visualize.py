import folium
import location2

# Example usage:
diagonal_size_inches = 1/1.3  # example diagonal in inches
aspect_ratio = (4, 3)  # example aspect ratio
altitude_m = 20        # Altitude in meters
focal_length_mm = 24    # Focal length in millimeters
drone_longitude = -20.249132
drone_latitude = 63.445533
image_width_x = 1920  # pixels
image_height_y = 1080  # pixels
px_x = 832.79596  # pixel x coordinate
px_y = 52.755585  # pixel y coordinate
bearing = -54 # Bearing in degrees

new_lon, new_lat = location2.calculate_offset(drone_longitude, drone_latitude, image_width_x, image_height_y, px_x, px_y, bearing, altitude_m, diagonal_size_inches, aspect_ratio, focal_length_mm)
print(f"The geographic coordinates of the point are Longitude: {new_lon}, Latitude: {new_lat}")
print(drone_longitude, drone_latitude, image_width_x, 
                                                        image_height_y, px_x, px_y, bearing, altitude_m, 
                                                        diagonal_size_inches, aspect_ratio, focal_length_mm)
print(f"new_lon: {new_lon}")
print(f"new_lat: {new_lat}")
# Create a map centered around the coordinates with a close zoom level

# Add satellite imagery layer
import folium
import location2
map = folium.Map(location=[drone_latitude, drone_longitude], zoom_start=17)
folium.TileLayer('Esri.WorldImagery').add_to(map)
# Add a marker for the drone
folium.Marker(
    [drone_latitude, drone_longitude],
    popup='Drone Location',
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(map)

folium.Marker(
    [new_lat, new_lon],
    popup='trash location',
    icon=folium.Icon(color='green', icon='info-sign')
).add_to(map)
map.save("map1.jpg")

# Display the map
map

