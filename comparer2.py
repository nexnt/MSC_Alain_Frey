import sqlite3
import cv2
import numpy as np
from math import radians, cos, sin, sqrt, atan2
import matplotlib.pyplot as plt
from geopy import distance

def calculate_distance(lon1, lat1, lon2, lat2):

    dist = distance.distance(( lat1, lon1),( lat2, lon2)).meters
    return dist

def debug_display_images(img1, img2):
    """Display two images side by side for debugging."""
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img1, cmap='gray')
    plt.title('Image 1')
    plt.subplot(1, 2, 2)
    plt.imshow(img2, cmap='gray')
    plt.title('Image 2')
    plt.show()

def remove_object(db_path, object_id):
    """Remove an object from the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM objects WHERE id=?", (object_id,))
    conn.commit()
    conn.close()

def find_and_remove_similar_objects(db_path, proximity_threshold=2, match_threshold=50):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, image, longitude, latitude FROM objects")
    objects = cursor.fetchall()

    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            id1, img1, lon1, lat1 = objects[i]
            id2, img2, lon2, lat2 = objects[j]
            if calculate_distance(lon1, lat1, lon2, lat2) <= proximity_threshold:
                img1 = cv2.imdecode(np.frombuffer(img1, np.uint8), cv2.IMREAD_GRAYSCALE)
                img2 = cv2.imdecode(np.frombuffer(img2, np.uint8), cv2.IMREAD_GRAYSCALE)
                num_matches = compare_images_with_sift(img1, img2)
                if num_matches > match_threshold:
                    print(f"Objects {id1} and {id2} are similar ({num_matches} matches).")
                    #debug_display_images(img1, img2)
                    remove_object(db_path, id2)  # Remove the second object
                    print(f"Removed object {id2} from the database.")
    conn.close()

import cv2

def compare_images_with_sift(img1, img2):
    # Initialize SIFT detector
    sift = cv2.SIFT_create()

    # Find the keypoints and descriptors with SIFT
    keypoints1, descriptors1 = sift.detectAndCompute(img1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(img2, None)

    # Ensure descriptors are not None (i.e., SIFT found features)
    if descriptors1 is not None and descriptors2 is not None:
        # Create BFMatcher object
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

        # Match descriptors
        matches = bf.match(descriptors1, descriptors2)

        # Filter matches based on the distance
        good_matches = [m for m in matches if m.distance < 300]  # Adjust distance threshold as needed

        return len(good_matches)
    else:
        # Return zero if no descriptors were found
        return 0



# Example usage
db_path = 'detected_objects.db'
find_and_remove_similar_objects(db_path)
