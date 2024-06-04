import folium
import location2
from geopy import distance
import math

def run_calculation(drone_longitude, drone_latitude, bearing_var, altitude_m_var, focal_var):

    result = location2.calculate_offset(drone_longitude, drone_latitude, image_width_x, image_height_y, px_x, px_y, bearing_var, altitude_m_var, diagonal_size_inches, aspect_ratio, focal_var)
    
    return result

# Example usage:
diagonal_size_inches = 1/1.3  # example diagonal in inches
aspect_ratio = (4, 3)  # example aspect ratio
altitude_m = 20        # Altitude in meters
focal_length_mm = 24    # Focal length in millimeters
drone_longitude = -21.702896
drone_latitude = 63.834375
image_width_x = 1920  # pixels
image_height_y = 1080  # pixels
px_x = 1910  # pixel x coordinate
px_y = 1040  # pixel y coordinate
bearing = 0 # Bearing in degrees



import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from geopy import distance
# Assuming location2.calculate_offset is already defined elsewhere and imported
# from your_module import location2

# Define default parameters
default_longitude = -21.702896
default_latitude = 68.834375
default_bearing = 0  # degrees
default_altitude = 20  # meters
default_focal_length_mm = 24    # Focal length in millimeters

# Define parameter ranges
longitude_range = np.linspace(default_longitude-(3*0.000020399), default_longitude+(3*0.000020399), 10, dtype=float)
latitude_range = np.linspace(default_latitude-(3*0.00000899), default_latitude+(3*0.00000899), 10, dtype=float)
bearing_range = np.linspace(default_bearing-10, default_bearing+10, 10)
altitude_range = np.linspace(default_altitude-5, default_altitude+5, 10)
focal_range = np.linspace(default_focal_length_mm-1, default_focal_length_mm+1, 10)

# Function to test variations in one parameter while keeping others constant
def test_parameter_variation(param_name, param_range):
    output_orig = run_calculation(default_longitude, default_latitude, default_bearing, default_altitude, default_focal_length_mm)
    results = []
    for value in param_range:
        if param_name == "bearing":
            output = run_calculation(default_longitude, default_latitude, value, default_altitude, default_focal_length_mm)
        elif param_name == "altitude":
            output = run_calculation(default_longitude, default_latitude, default_bearing, value, default_focal_length_mm)
        elif param_name == "focal_length":
            output = run_calculation(default_longitude, default_latitude, default_bearing, default_altitude, value)    
        
        dist = distance.distance(output,output_orig).meters
        

        delta_lon_m = distance.distance((output[0], output_orig[1]),output_orig).meters
        #print(delta_lon_m)
        delta_lat_m = distance.distance((output_orig[0], output[1]),output_orig).meters
        #print(delta_lat_m)
        results.append((value, output[0], output[1], dist, delta_lon_m, delta_lat_m))

    df = pd.DataFrame(results, columns=[param_name, 'new_lon', 'new_lat','delta_m','delta_lon_m','delta_lat_m'])

    
    

    return df

# Updated plotting function to handle only delta_lon and delta_lat
def plot_results(df, param_name):
    if param_name in ['bearing', 'altitude', 'focal_length']:  # Only plot for bearing and altitude changes
        fig, ax = plt.subplots(1, 3, figsize=(10, 5))  # Adjusted for two plots
        titles = ['Delta Longitude (m)','Delta Latitude (m)','Delta Absolute (m)']
        columns = ['delta_lon_m', 'delta_lat_m', 'delta_m']
        for i, column in enumerate(columns):
            ax[i].plot(df[param_name], df[column])
            ax[i].set_title(titles[i])
            ax[i].set_xlabel(param_name)
            ax[i].set_ylabel(column)
        plt.tight_layout()
        plt.show()

# Run tests for each parameter
for param, param_range in zip(['bearing', 'altitude', 'focal_length'], [bearing_range, altitude_range, focal_range]):
    df = test_parameter_variation(param, param_range)
    plot_results(df, param)
    if param in ['bearing', 'altitude', 'focal_length']:  # Only print dataframe for bearing and altitude
        print(df)