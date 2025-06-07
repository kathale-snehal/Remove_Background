
import rembg
import numpy as np
from PIL import Image
import onnxruntime as ort

# Load the input image
input_image = Image.open('img/pose.png')
# print(input_image.shape)

# Convert the input image to a numpy array
input_array = np.array(input_image)

# Apply background removal using rembg
output_array = rembg.remove(input_array)

# Create a PIL Image from the output array
output_image = Image.fromarray(output_array)

# Save the output image
output_image.save('output/output_image.png')