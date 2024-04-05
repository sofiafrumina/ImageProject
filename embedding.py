import os
import torch
from torch.utils.data import Dataset, DataLoader
import PIL
import pickle
from tqdm import tqdm
from clip import clip

class Images(Dataset):
    def __init__(self, image_list, transform):
        self.image_list = image_list
        self.transform = transform

    def __len__(self):
        return len(self.image_list)

    def __getitem__(self, idx):
        image_path = self.image_list[idx]
        image = PIL.Image.open(image_path)
        image = self.transform(image)
        data = {'image': image, 'img_path': image_path}
        return data

if __name__ == '__main__':
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load('ViT-B/32', device, jit=False)
    print(f'Device used: {device}')

    folder_path = 'images/paints'
    image_list = [folder_path + '/' + file for file in os.listdir(folder_path)]

    print('Attempting to open images...')
    cleaned_image_list = []
    for image_path in image_list:
        try:
            PIL.Image.open(image_path)
            cleaned_image_list.append(image_path)
        except:
            print(f"Failed for {image_path}")

    print(f"There are {len(cleaned_image_list)} images that can be processed")
    dataset = Images(cleaned_image_list, preprocess)

    dataloader = DataLoader(dataset, batch_size=256, shuffle=True)

    print("Processing images...")
    image_paths = []
    embeddings = []
    for data in tqdm(dataloader):
        with torch.no_grad():
            X = data['image'].to(device)
            image_embedding = model.encode_image(X)
            img_path = data['img_path']
            image_paths.extend(img_path)
            embeddings.extend([torch.Tensor(x).unsqueeze(0).cpu() for x in image_embedding.tolist()])

    image_embeddings = dict(zip(image_paths, embeddings))

    # Save to pickle file for the app
    print("Saving image embeddings")
    with open('embeddings.pkl', 'wb') as f:
        pickle.dump(image_embeddings, f)