from PIL import Image
import os
import math

def combine_images(folder_path, output_path, ignore_list=None, grid_size=None):
    # Set a default ignore list if none provided
    if ignore_list is None:
        ignore_list = []

    # List PNG images in folder, excluding any in the ignore list
    images = [
        os.path.join(folder_path, f) for f in os.listdir(folder_path) 
        if f.endswith('.png') and f not in ignore_list
    ]
    
    if not images:
        print("No images found in the specified directory!")
        return

    # Open images and convert to the same mode
    images = [Image.open(img).convert('RGBA') for img in images]

    # Determine grid size if not specified
    if grid_size is None:
        num_images = len(images)
        grid_size = (int(math.ceil(math.sqrt(num_images))),) * 2

    # Determine max dimensions of images in the grid
    max_width = max(img.size[0] for img in images)
    max_height = max(img.size[1] for img in images)

    # Create output image
    grid_img = Image.new('RGBA', (max_width * grid_size[1], max_height * grid_size[0]))

    for index, image in enumerate(images):
        x = index % grid_size[1] * max_width
        y = index // grid_size[1] * max_height
        grid_img.paste(image, (x, y))

    grid_img.save(output_path)
    print(f"Combined image saved as {output_path}")

# Usage example
combine_images('/Users/alainfrey/Documents/code/mscthesis/runs/segment/val12', 'output_image_val8.png', ignore_list=['confusion_matrix_normalized.png', 'confusion_matrix.png', 'BoxF1_curve.png', 'BoxP_curve.png','BoxPR_curve.png', 'BoxR_curve.png'], grid_size=(2, 4))
