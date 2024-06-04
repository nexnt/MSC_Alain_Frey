import sqlite3
import cv2
import numpy as np

import math

def haversine(lon1, lat1, lon2, lat2):
    """Calculate the great-circle distance between two points on the Earth specified in decimal degrees."""
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    # Radius of Earth in kilometers. Use 6371 for kilometers or 6371000 for meters
    r = 6371000
    return c * r



def fetch_and_compare_objects_orb(db_path, proximity_threshold=1, orb_threshold=30):
    """Fetches objects from the database and compares them for similarity based on location and ORB feature matching.

    Args:
    db_path (str): Path to the SQLite database file.
    proximity_threshold (int): Maximum distance in meters between coordinates to consider similar.
    orb_threshold (int): Maximum distance for ORB feature matching.

    Returns:
    list: Pairs of similar objects (ids from the database).
    """
    print("Connecting to the database...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print("Fetching data from the database...")
    cursor.execute("SELECT id, image, longitude, latitude FROM objects")
    items = cursor.fetchall()
    similar_pairs = []

    # Initialize ORB detector
    orb = cv2.ORB_create()
    print("ORB detector initialized.")

    # Helper function to calculate similarity based on ORB features
    def are_images_similar(img1, img2):
        print("Decoding images and detecting features...")
        img1 = cv2.imdecode(np.frombuffer(img1, np.uint8), cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imdecode(np.frombuffer(img2, np.uint8), cv2.IMREAD_GRAYSCALE)
        keypoints1, descriptors1 = orb.detectAndCompute(img1, None)
        keypoints2, descriptors2 = orb.detectAndCompute(img2, None)
        if descriptors1 is None or descriptors2 is None:
            print("No features found in one or both images.")
            return False
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(descriptors1, descriptors2)
        if matches:
            distances = [m.distance for m in matches]
            average_distance = sum(distances) / len(distances)
            print(f"Average descriptor distance: {average_distance}")
            return average_distance < orb_threshold
        else:
            print("No matches found.")
            return False

    print("Comparing objects...")
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            id1, img1, lon1, lat1 = items[i]
            id2, img2, lon2, lat2 = items[j]
            # Check geographic proximity using the Haversine formula
            if haversine(lon1, lat1, lon2, lat2) <= proximity_threshold:
                print(f"Comparing objects {id1} and {id2} for similarity...")
                if are_images_similar(img1, img2):
                    print(f"Objects {id1} and {id2} are similar.")
                    similar_pairs.append((id1, id2))
                else:
                    print(f"Objects {id1} and {id2} are not similar.")

    conn.close()
    print("Database connection closed.")
    return similar_pairs


fetch_and_compare_objects_orb(db_path = 'detected_objects.db', proximity_threshold=1 , orb_threshold=30)
