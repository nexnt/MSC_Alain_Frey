import sqlite3
from geopy.distance import geodesic

def get_data():
    """Fetch images and their metadata from the SQLite database."""
    conn = sqlite3.connect('detected_objects.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, image, longitude, latitude, altitude FROM objects")
    data = cursor.fetchall()
    conn.close()
    return data

def cluster_data(data, proximity):
    """Cluster data points based on their geographical proximity."""
    clusters = []
    while data:
        base_point = data.pop(0)
        cluster = [base_point]
        to_remove = []
        for point in data:
            if geodesic((base_point[3], base_point[2]), (point[3], point[2])).meters <= proximity:
                cluster.append(point)
                to_remove.append(point)
        data = [d for d in data if d not in to_remove]
        clusters.append(cluster)
    return clusters

def create_cluster_db(cluster, cluster_id):
    """Create a new SQLite file for a cluster of objects."""
    conn = sqlite3.connect(f'cluster_{cluster_id}.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE objects (
            id INTEGER PRIMARY KEY,
            image BLOB,
            longitude REAL,
            latitude REAL,
            altitude REAL
        )
    """)
    cursor.executemany("INSERT INTO objects (id, image, longitude, latitude, altitude) VALUES (?, ?, ?, ?, ?)", cluster)
    conn.commit()
    conn.close()

def main(proximity):
    data = get_data()
    clusters = cluster_data(data, proximity)
    for idx, cluster in enumerate(clusters):
        create_cluster_db(cluster, idx)
    print(f'{len(clusters)} clusters created.')

if __name__ == "__main__":
    main(proximity=2)  # Specify proximity in meters
