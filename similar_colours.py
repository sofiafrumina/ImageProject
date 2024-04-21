import cv2
import numpy as np
import os

def convert_to_lab(image_path):
    image = cv2.imread(image_path)
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    return lab_image

def calculate_average_lab(lab_image):
    avg_lab = np.mean(lab_image, axis=(0, 1))
    return avg_lab

def compute_color_difference(avg_lab1, avg_lab2):
    color_difference = np.linalg.norm(avg_lab1 - avg_lab2)
    return color_difference

# Load and convert image1.jpg to CIELAB
image1_path = 'images/newPaints/202.png'
lab_image1 = convert_to_lab(image1_path)
avg_lab1 = calculate_average_lab(lab_image1)

# Directory containing all images
images_dir = 'images/newPaints'

# Initialize a list to store image names and their color differences
image_diffs = []

# Iterate over all images in the directory
for filename in os.listdir(images_dir):
    if filename.endswith(".png") and  filename != os.path.basename(image1_path):
        image_path = os.path.join(images_dir, filename)
        lab_image = convert_to_lab(image_path)
        avg_lab = calculate_average_lab(lab_image)
        color_difference = compute_color_difference(avg_lab1, avg_lab)
        image_diffs.append((filename, color_difference))

# Sort the images by color difference and select the 3 most similar
image_diffs.sort(key=lambda x: x[1])
most_similar_images = [image_name for image_name, _ in image_diffs[:3]]

print(f"The 3 images most similar to {image1_path} are:")
for image_name in most_similar_images:
    print(image_name)