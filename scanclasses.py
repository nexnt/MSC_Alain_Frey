import os
from collections import defaultdict

def count_class_occurrences(directory):
    class_counts = defaultdict(int)  # Dictionary to store class counts
    file_count = 0  # Counter for files processed
    errors = 0  # Counter for errors

    # Walk through the directory and find all .txt files
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        lines = f.readlines()

                    for line in lines:
                        if line.strip():  # Ensure line is not empty
                            parts = line.split()
                            if len(parts) == 5:  # Check if line is correctly formatted
                                class_id = parts[0]
                                class_counts[class_id] += 1
                            else:
                                errors += 1
                                print(f"Skipping malformed line in {file_path}: {line.strip()}")
                    file_count += 1
                except Exception as e:
                    errors += 1
                    print(f"Error processing {file_path}: {e}")

    return class_counts, file_count, errors

# Path to the directory containing YOLO format .txt files
directory_path = '/Users/alainfrey/Documents/yolo/datasets/roboflow2/test'

# Scan files and count class occurrences
class_counts, file_count, error_count = count_class_occurrences(directory_path)

# Output the results
print(f"Total number of .txt files scanned: {file_count}")
print(f"Total number of errors encountered: {error_count}")
print("Occurrences per class:")
for class_id, count in sorted(class_counts.items(), key=lambda item: item[0]):
    print(f"Class ID {class_id}: {count} occurrences")

