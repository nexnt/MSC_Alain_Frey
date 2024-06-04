import cv2
import pysrt
from ultralytics import YOLO
import re
import location2
from collections import deque
from geopy.distance import geodesic
from math import atan2, radians, degrees, cos, sin
import matplotlib.pyplot as plt
import cv2
import random
import sqlite3

def parse_metadata(metadata_string):

    # Removing HTML tags for cleaner text processing
    clean_text = re.sub(r'<[^>]+>', '', metadata_string)

    # Dictionary to store the values
    geo_data = {}

    # Extracting the numbers for specific keys and storing them as floats in the dictionary
    def extract_float(key, pattern):
        match = re.search(pattern, clean_text)
        return float(match.group(1)) if match else None

    geo_data['latitude'] = extract_float('latitude', r'latitude: ([\d\.\-]+)')
    geo_data['longitude'] = extract_float('longitude', r'longitude: ([\d\.\-]+)')
    geo_data['rel_alt'] = extract_float('rel_alt', r'rel_alt: ([\d\.\-]+)')
    geo_data['abs_alt'] = extract_float('abs_alt', r'abs_alt: ([\d\.\-]+)')

    return geo_data

# Function to process frames
def process_frame(frame, geo_data):

    # Constants
    diagonal_size_inches = 1/1.3  # example diagonal in inches
    aspect_ratio = (4, 3)  # example aspect ratio
    focal_length_mm = 24    # Focal length in millimeters
    
    bearing = geo_data['bearing']
    drone_longitude = geo_data['longitude']
    drone_latitude = geo_data['latitude']
    drone_altitude = geo_data['abs_alt']
    # Perform detection
    results = model.track(frame, imgsz=1280, persist=True)
    image_height_y, image_width_x, c = frame.shape
    # List to store each object's data
    detected_objects = []


    boxes = results[0].boxes.xywh.cpu()
    track_ids = results[0].boxes.id.int().cpu().tolist()

    # Plot the tracks
    for box, track_id in zip(boxes, track_ids):       
        px_x, px_y, w, h = box  # Extract bounding box coordinates and size
        #x1, y1, x2, y2 =box.xyxy[0].numpy()
        # Calculate the geographic location of the detected object
        new_lon, new_lat= location2.calculate_offset(drone_longitude, drone_latitude, image_width_x, 
                                                    image_height_y, px_x, px_y, bearing, altitude_m, 
                                                    diagonal_size_inches, aspect_ratio, focal_length_mm)
        #print(f"The geographic coordinates of the point are Longitude: {new_lon}, Latitude: {new_lat}")

        # Extract the part of the image enclosed by the bounding box
        x1, y1 = int(px_x - w/2), int(px_y - h/2)
        x2, y2 = int(px_x + w/2), int(px_y + h/2)
        #cropped_image = frame[x1:y1, x2:y2].copy()
        cropped_image = frame[y1:y2, x1:x2].copy()

        # Store the bounding box, geographic coordinates, and image segment
        detected_objects.append({
            'bbox': (x1, y1, x2, y2),
            'bboxcenter': (px_x, px_y),
            'coordinates': {'longitude': new_lon, 'latitude': new_lat},
            'coordinates_drone': {'longitude': drone_longitude, 'latitude': drone_latitude},
            'abs_alt': drone_altitude,
            'image_segment': cropped_image,
            'image': frame,
            'bearing': bearing,
            'trackid': track_id
        })

    return detected_objects

# Function to calculate bearing between two points
def calculate_bearing(lat1, lon1, lat2, lon2):
    """Calculate the bearing between two points on the earth."""
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dLon = lon2 - lon1
    x = atan2(sin(dLon) * cos(lat2), cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dLon))
    return degrees(x)

# Function to display frame with speed and bearing
def display_frame(frame, speed, bearing, current_altitude, objects=[]):
    """Display the video frame with speed and bearing information overlay."""
        
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, f'Speed: {speed:.2f} m/s', (10, 30), font, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, f'Bearing: {bearing:.2f} degrees', (10, 60), font, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, f'Altitude: {current_altitude:.2f} m', (10, 90), font, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

    # Draw bounding boxes and display geographic coordinates
    for obj in objects:
        bbox = obj['bbox']
        coordinates = obj['coordinates']
        longitude, latitude = coordinates['longitude'], coordinates['latitude']
        
        # Draw rectangle around the object
        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
        
        # Display geographic coordinates on the frame
        coord_text = f"ID: {obj['trackid']:.6f},Lon: {longitude:.6f}, Lat: {latitude:.6f}"
        cv2.putText(frame, coord_text, (bbox[0], bbox[1] - 10), font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)


    cv2.imshow('Video', frame)


def calculate_frames_to_skip(speed, gsd, image_height, frame_rate):
    """
    Calculate the number of frames to skip to avoid overlap in video frames based on speed, GSD, and image size.

    Parameters:
    speed (float): Speed of the camera relative to the ground in meters/second.
    gsd (float): Ground Sample Distance in meters.
    image_height (int): The height of the image in pixels.
    frame_rate (float): Video frame rate in frames per second.

    Returns:
    int: The number of frames to skip to avoid overlap.
    """
    ground_distance_covered = gsd * image_height  # Total vertical distance covered by the image
    time_to_cover_distance = ground_distance_covered / speed  # Time required to cover this distance
    frames_to_skip = int(frame_rate * time_to_cover_distance)  # Calculate frames to skip

    return frames_to_skip


def plot_detected_objects(detected_objects):
    """
    Plots images of detected objects with bounding boxes and coordinates annotated.

    Args:
    detected_objects (list): A list of dictionaries, each containing 'image_segment' and 'coordinates'.
    """

    # Check if there are fewer than 10 objects, if so, use the length of the list
    num_objects = min(10, len(detected_objects))

    # Select 10 random objects if there are at least 10, otherwise select all
    if num_objects < 10:
        selected_objects = detected_objects  # Use all objects if fewer than 10
    else:
        selected_objects = random.sample(detected_objects, 10)

    num_objects = len(selected_objects)
    
    fig, axes = plt.subplots(1, num_objects, figsize=(1 * num_objects, 2))  # Adjust size as needed

    if num_objects == 1:
        axes = [axes]  # Make it iterable for a single subplot scenario

    for ax, obj in zip(axes, selected_objects):
        # Convert BGR image to RGB
        image = cv2.cvtColor(obj['image_segment'], cv2.COLOR_BGR2RGB)
        ax.imshow(image)
        ax.axis('off')  # Hide axis
        longitude, latitude = obj['coordinates']['longitude'], obj['coordinates']['latitude']
        ax.set_title(f"Lon: {longitude:.6f}, Lat: {latitude:.6f}", fontsize=6)

    plt.show()


def initialize_and_insert_objects(db_path, detected_objects):
    """Initializes the database if not already set up and inserts detected objects.
    
    Args:
    db_path (str): Path to the SQLite database file.
    detected_objects (list): A list of dictionaries containing detected object data.
    """
    # Establish connection and create table if it does not exist
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS objects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image BLOB,
            longitude REAL,
            latitude REAL,
            altitude REAL,
            bbox TEXT
        )
    ''')
    conn.commit()

    # Function to insert a single object into the database
    def insert_object(image, longitude, latitude, altitude, bbox):
        # Convert image to binary data
        _, buffer = cv2.imencode('.jpg', image)
        image_data = buffer.tobytes()

        # Convert bounding box data to a string format
        bbox_str = ','.join(map(str, bbox))

        # Insert data into the database
        cursor.execute('''
            INSERT INTO objects (image, longitude, latitude, altitude, bbox)
            VALUES (?, ?, ?, ?, ?)
        ''', (image_data, longitude, latitude, altitude, bbox_str))
        conn.commit()

    # Process each detected object
    for obj in detected_objects:
        print('inserting obj')
        print(obj)
        insert_object(
            obj['image_segment'],
            obj['coordinates']['longitude'],
            obj['coordinates']['latitude'],
            obj['abs_alt'],
            obj['bbox']
        )

    # Close the database connection
    conn.close()


def plot_flight_path(flight_path,detected_objects):
    import folium
    import location2
    
    map = folium.Map(location=flight_path[0], zoom_start=17, tiles=tileurl, attr='Mapbox', max_zoom = 19)
    #map = folium.Map(location=flight_path[0], zoom_start=17)
    folium.TileLayer('Esri.WorldImagery').add_to(map)
    # Add a marker for the drone

    # Add a line to the map to represent the flight path
    folium.PolyLine(flight_path, color='blue', weight=5, opacity=0.8).add_to(map)

    # Optionally, add markers at each coordinate point
    for obj in detected_objects:
        coordinates = obj['coordinates']['latitude'], obj['coordinates']['longitude']
        folium.Marker(
            location=coordinates,
            
            icon=folium.Icon(icon='plane', prefix='fa', color='red')
        ).add_to(map)
        
    map.save("save_file.html")

if __name__ == "__main__":
    # Initialize a deque to store the last 90 coordinates along with timestamps
    coords_window = deque(maxlen=90)

    # Initialize the YOLOv8 model
    model = YOLO("/Users/alainfrey/Library/CloudStorage/GoogleDrive-alain.frey@outlook.com/My Drive/detect1280b16ep200custom138/train/weights/best.pt")  # Adjust the model path and name as necessary

    # Load SRT file
    subs = pysrt.open('/Users/alainfrey/Lichtwinkel Dropbox/Alain Frey/thesis/strandkirkja/good/DJI_0210.srt')

    # Capture video
    cap = cv2.VideoCapture('/Users/alainfrey/Lichtwinkel Dropbox/Alain Frey/thesis/strandkirkja/good/DJI_0210.MP4')
    #/Users/alainfrey/Lichtwinkel Dropbox/Alain Frey/thesis/strandkirkja/good/DJI_0208.MP4
    #/Users/alainfrey/Lichtwinkel Dropbox/Alain Frey/thesis/trashbeach/DJI_0159.MP4
    frame_id = 0

    sensor_dimension_x_mm, sensor_dimension_y_mm = 15.630769230769229, 11.723076923076922
    focal_length_mm = 24    # Focal length in millimeters

    detected_objects = []
    flight_path = []

    # Main loop to process video frames
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Get current time in seconds
            current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
            sub = subs.at(seconds=current_time)
            fps = cap.get(cv2. CAP_PROP_FPS)

            if sub and sub.text.strip():
                # Assuming parse_metadata function correctly extracts the latitude and longitude
                geo_data = parse_metadata(sub.text)
                current_position = (geo_data['latitude'], geo_data['longitude'])
                
                # Add current position and time to the deque
                coords_window.append((current_position, current_time))

                # Ensure we have at least two points to calculate speed and bearing
                if len(coords_window) >= 2:
                    # Use the first and the last item in the deque for calculations
                    (start_pos, start_time), (end_pos, end_time) = coords_window[0], coords_window[-1]

                    # Calculate distance in meters
                    distance = geodesic(start_pos, end_pos).meters

                    # Calculate time difference in seconds
                    time_diff = end_time - start_time

                    # Calculate speed in meters per second
                    speed = distance / time_diff if time_diff > 0 else 0

                    geo_data['speed'] = speed

                    # Calculate bearing in degrees
                    bearing = calculate_bearing(start_pos[0], start_pos[1], end_pos[0], end_pos[1])

                    geo_data['bearing'] = bearing

                    
                    
                    geo_data['abs_alt'] = 15

                    altitude_m = geo_data['abs_alt']


                    #print(skip_frames)
                    # Process only every 30th frame
                    skip_detect = 0
                    flight_path.append(current_position)
                    skip_frames=5
                    if frame_id % skip_frames == 0:
                        objects = process_frame(frame, geo_data)
                        display_frame(frame, speed, bearing, altitude_m, objects)
                        
                        
                        # Parse the metadata
                        for obj in objects:
                            detected_objects.append(obj)

                                

                    
                        
                    




            frame_id += 1

            # Break the loop by pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                #print(detected_objects)
                plot_flight_path(flight_path, detected_objects)
                plot_detected_objects(detected_objects)
                
                db_path = 'detected_objects.db'
                #initialize_and_insert_objects(db_path, detected_objects)


                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
