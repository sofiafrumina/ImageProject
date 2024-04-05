import os
import imagehash
from PIL import Image
import itertools
import csv

# Change this to your image directory
image_directory = 'images/example_folder'

# Change the working directory to the image directory
os.chdir(image_directory)

# List all files in the directory
image_files = os.listdir()

# Initialize lists to store duplicates and their hashes
duplicates = []
hashes = []

# Compute hashes for each image
for file in image_files:
    try:
        with Image.open(file) as img:
            hash_value = imagehash.phash(img)
            hashes.append((file, hash_value))
    except IOError:
        print(f"Error opening {file}")

# Compare hashes to find duplicates
for pair1, pair2 in itertools.combinations(hashes, 2):
    file1, hash1 = pair1
    file2, hash2 = pair2
    hash_difference = hash1 - hash2

    # Adjust the threshold based on how strict you want the duplicate detection to be
    if hash_difference < 1:
        print(f"Images are similar: {file1}, {file2}")
        duplicates.append((file1, file2))