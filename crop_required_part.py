from PIL import Image

def extract_and_crop_non_transparent_pixels(input_path, output_path):
    # Open image and convert to RGBA mode
    image = Image.open(input_path).convert("RGBA")
    pixels = image.load()

    # Find the bounding box of non-transparent and non-black pixels
    min_x, min_y, max_x, max_y = image.width, image.height, 0, 0
    has_content = False  # To check if there's any non-transparent pixel

    for x in range(image.width):
        for y in range(image.height):
            r, g, b, a = pixels[x, y]
            if (r, g, b) != (0, 0, 0) or a != 0:
                has_content = True
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)

    # If no non-transparent pixels are found, return an empty image
    if not has_content:
        print("No non-transparent pixels found.")
        return

    # Crop the image to the detected bounding box
    cropped_image = image.crop((min_x, min_y, max_x + 1, max_y + 1))

    # Save the cropped image
    cropped_image.save(output_path)
    print(f"Extraction complete! Cropped image saved at {output_path}")

# Paths
input_path = "./output/output.png"  # Background removed image
output_path = "./output/extracted_cropped.png"  # Cropped extracted image

# Run function
extract_and_crop_non_transparent_pixels(input_path, output_path)
