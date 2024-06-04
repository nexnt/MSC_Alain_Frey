import os

def replace_class(directory, old_class_id='1', new_class_id='0'):
    file_count = 0  # Counter for files processed
    lines_changed = 0  # Counter for lines changed
    errors = 0  # Counter for errors

    # Walk through the directory and find all .txt files
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        lines = f.readlines()

                    new_lines = []
                    for line in lines:
                        if line.strip():  # Ensure line is not empty
                            parts = line.split()
                            if len(parts) == 5:  # Check if line is correctly formatted
                                # Check if the current class ID is the old class ID
                                if parts[0] == old_class_id:
                                    parts[0] = new_class_id  # Replace it with the new class ID
                                    lines_changed += 1
                                new_line = ' '.join(parts) + '\n'
                                new_lines.append(new_line)
                            else:
                                errors += 1
                                print(f"Skipping malformed line in {file_path}: {line.strip()}")

                    # Write the modified lines back to the file
                    with open(file_path, 'w') as f:
                        f.writelines(new_lines)

                    file_count += 1
                except Exception as e:
                    errors += 1
                    print(f"Error processing {file_path}: {e}")

    return file_count, lines_changed, errors

# Path to the directory containing YOLO format .txt files
directory_path = '/Users/alainfrey/Documents/yolo/datasets/export5seg/'

# Replace class '1' with class '0'
file_count, lines_changed, error_count = replace_class(directory_path, '1', '0')

# Output the results
print(f"Total number of .txt files processed: {file_count}")
print(f"Total number of lines changed: {lines_changed}")
print(f"Total number of errors encountered: {error_count}")
