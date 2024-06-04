import cv2
import pysrt
from collections import deque
from geopy.distance import geodesic
from math import atan2, radians, degrees, cos, sin
import re

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


# Load SRT file
subs = pysrt.open('/Users/alainfrey/Lichtwinkel Dropbox/Alain Frey/thesis/trashbeach/DJI_0174.srt')

# Capture video
cap = cv2.VideoCapture('/Users/alainfrey/Lichtwinkel Dropbox/Alain Frey/thesis/trashbeach/DJI_0174.MP4')

