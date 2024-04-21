import cv2
import numpy as np
import os
import pickle

class ImageIndexer:
    def __init__(self, index_file=None):
        self.index = {}
        self.orb = cv2.ORB_create()
        self.index_file = index_file

    def index_images(self, images_directory):
        for filename in os.listdir(images_directory):
            filepath = os.path.join(images_directory, filename)
            if os.path.isfile(filepath):
                image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                if image is not None:
                    keypoints, descriptors = self.orb.detectAndCompute(image, None)
                    self.index[filename] = descriptors

    def save_index(self):
        if self.index_file:
            with open(self.index_file, 'wb') as f:
                pickle.dump(self.index, f)
            print("Index saved successfully.")

    def load_index(self):
        if self.index_file and os.path.exists(self.index_file):
            with open(self.index_file, 'rb') as f:
                self.index = pickle.load(f)
            print("Index loaded successfully.")

    def search(self, query_image_path, top_n=5):
        query_image = cv2.imread(query_image_path, cv2.IMREAD_GRAYSCALE)
        if query_image is None:
            print("Error: Unable to read the query image.")
            return []

        keypoints, query_descriptors = self.orb.detectAndCompute(query_image, None)

        results = []
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        for filename, image_descriptors in self.index.items():
            matches = bf.match(query_descriptors, image_descriptors)
            similarity = sum(match.distance for match in matches) / len(matches)
            results.append((filename, similarity))

        results.sort(key=lambda x: x[1])

        return results[:top_n]

if __name__ == "__main__":
    images_directory = "images/newPaints"  # Directory containing images
    query_image_path = "images/newPaints/202.png"  # Path to the query image
    index_file = "images/image_index.pkl"  # File to save/load index

    indexer = ImageIndexer(index_file)

    if os.path.exists(index_file):
        indexer.load_index()
    else:
        indexer.index_images(images_directory)
        indexer.save_index()

    search_results = indexer.search(query_image_path)

    if search_results:
        print("Search results:")
        for filename, similarity in search_results:
            print(f"Image: {filename}, Similarity: {similarity}")
    else:
        print("No matching images found.")