import cv2
import numpy as np

# Load the image with the alpha channel
img_path = 'images/newPaints/1.png'
img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

# Check if the image has an alpha channel
if img.shape[2] == 4:
    # Extract the alpha channel
    alpha_channel = img[:, :, 3]
    
    # Threshold the alpha channel to create a binary mask
    # Adjust the threshold value as needed
    _, mask = cv2.threshold(alpha_channel, 200, 255, cv2.THRESH_BINARY)
    
    # Save the mask
    cv2.imwrite('images/mask.png', mask)
else:
    print("The image does not have an alpha channel.")
