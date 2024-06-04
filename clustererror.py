import sqlite3
from geopy.distance import geodesic
import numpy as np
import glob

def get_cluster_data(cluster_id):
    """Fetch images and their metadata from a clustered SQLite database."""
    conn = sqlite3.connect(f'cluster_{cluster_id}.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, image, longitude, latitude, altitude FROM objects")
    data = cursor.fetchall()
    conn.close()
    return data

def calculate_centroid(cluster):
    """Calculate the centroid (average location) of a cluster."""
    longitudes = [point[2] for point in cluster]
    latitudes = [point[3] for point in cluster]
    centroid = (np.mean(latitudes), np.mean(longitudes))
    return centroid

def calculate_errors(cluster, centroid):
    """Calculate the distances from each point to the centroid for a cluster."""
    errors = [geodesic((point[3], point[2]), centroid).meters for point in cluster]
    return errors

def calculate_mean_and_std_error(errors):
    """Calculate the mean error and standard deviation of errors for a cluster."""
    mean_error = np.mean(errors)
    std_deviation = np.std(errors)
    return mean_error, std_deviation

def find_furthest_outlier(cluster, errors):
    """Find the furthest outlier in a cluster based on the errors."""
    max_error = max(errors)
    max_error_index = errors.index(max_error)
    furthest_outlier = cluster[max_error_index]
    return furthest_outlier, max_error

def main():
    cluster_files = glob.glob('cluster_*.db')
    for cluster_file in cluster_files:
        cluster_id = cluster_file.split('_')[1].split('.')[0]
        cluster_data = get_cluster_data(cluster_id)
        centroid = calculate_centroid(cluster_data)
        errors = calculate_errors(cluster_data, centroid)
        mean_error, std_deviation = calculate_mean_and_std_error(errors)
        furthest_outlier, max_error = find_furthest_outlier(cluster_data, errors)
        print(f'Cluster {cluster_id}:')
        print(f'  Mean error is {mean_error:.2f} meters')
        print(f'  Standard deviation is {std_deviation:.2f} meters')
        print(f'  Furthest outlier is at ID {furthest_outlier[0]} with an error of {max_error:.2f} meters')
    print(f'{len(cluster_files)} clusters processed.')

if __name__ == "__main__":
    main()
