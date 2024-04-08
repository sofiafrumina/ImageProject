import os
import splitfolders
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder

print("Starting script...")

# Specify the path to your dataset
input_folder = 'images/images_classes'

# Specify the output path where the split datasets will be stored
output_folder = 'split_image_classes'

# Check if the output folder already exists
if not os.path.exists(output_folder):
    print("Splitting dataset into training and validation sets...")
    # Split the dataset with a ratio of 80% for training and 20% for validation
    splitfolders.ratio(input_folder, output=output_folder, seed=42, ratio=(.8, .2))
else:
    print(f"The folder '{output_folder}' already exists. Skipping the splitting process.")

# Load the pre-trained ResNet18 model
print("Loading pre-trained ResNet18 model...")
base_model = models.resnet18(pretrained=True)

# Modify the model to remove the top layer and add our custom layers
num_classes = len(os.listdir('images/images_classes')) # Adjust this to match your dataset
print(f"Modifying model for {num_classes} classes...")

# Freeze all the parameters in the base model
for param in base_model.parameters():
    param.requires_grad = False

# Replace the final fully connected layer
num_ftrs = base_model.fc.in_features
base_model.fc = nn.Sequential(
    nn.Linear(num_ftrs, 1024),
    nn.ReLU(),
    nn.Linear(1024, num_classes)
)

# Define the data augmentation and normalization for the training data
train_transforms = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Define the data augmentation and normalization for the validation data
val_transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Load the training data
print("Loading training data...")
train_data = ImageFolder(os.path.join(output_folder, 'train'), transform=train_transforms)

# Load the validation data
print("Loading validation data...")
val_data = ImageFolder(os.path.join(output_folder, 'val'), transform=val_transforms)

# Create data loaders
print("Creating data loaders...")
train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
val_loader = DataLoader(val_data, batch_size=32, shuffle=False)

# Define the loss function and optimizer
print("Defining loss function and optimizer...")
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(base_model.parameters(), lr=0.0001)

# Check if CUDA is available and set the device accordingly
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Move the model to the device
base_model = base_model.to(device)

# Train the model
print("Starting training...")
for epoch in range(10): # loop over the dataset multiple times
    running_loss = 0.0
    for i, data in enumerate(train_loader, 0):
        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data[0].to(device), data[1].to(device) # Move data to the device
        
        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = base_model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if i % 20 == 19:    # print every 2000 mini-batches
            print('[%d, %5d] loss: %.3f' %
                 (epoch + 1, i + 1, running_loss / 20))
            running_loss = 0.0
print('Finished Training')

# Evaluate the model on the validation set
print("Evaluating model on validation set...")
base_model.eval() # Set the model to evaluation mode
correct = 0
total = 0
with torch.no_grad():
    for data in val_loader:
        images, labels = data[0].to(device), data[1].to(device) # Move data to the device
        outputs = base_model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print('Accuracy of the network on the validation images: %d %%' % (100 * correct / total))

# Save the model
print("Saving model...")
torch.save(base_model.state_dict(), 'model_weights.pth')
print("Model saved.")
