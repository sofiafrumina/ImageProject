import torch
from clip import clip
import pickle
from PIL import Image
import numpy as np

# Load the CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load('ViT-B/32', device, jit=False)

# Load the saved embeddings
with open('./embeddings.pkl', 'rb') as f:
    image_embeddings = pickle.load(f)

# Function to encode text into an embedding
def encode_text(text):
    with torch.no_grad():
        text_input = clip.tokenize([text]).to(device)
        text_embedding = model.encode_text(text_input)
    return text_embedding

# Function to compare embeddings
def compare_embeddings(text_embedding, image_embeddings):
    similarities = []
    for img_path, img_embedding in image_embeddings.items():
        similarity = torch.nn.functional.cosine_similarity(text_embedding, img_embedding)
        similarities.append((img_path, similarity.item()))
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities

# Example usage
search_text = "oil paints"
text_embedding = encode_text(search_text)
similarities = compare_embeddings(text_embedding, image_embeddings)

# Display the most similar images
for img_path, similarity in similarities[:5]: # Display top 5 results
    print(f"Image: {img_path}, Similarity: {similarity}")