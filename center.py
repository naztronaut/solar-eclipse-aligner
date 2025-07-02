import os
import cv2
import numpy as np

def find_sun(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)

    # Use HoughCircles to detect circles (the sun)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=100,
                               param1=50, param2=30, minRadius=50, maxRadius=200)

    # If no circles are found, return None
    if circles is None:
        return None
    
    # Extract the coordinates and radius of the sun
    x, y, radius = circles[0][0].astype(int)

    return x, y, radius

def create_eclipse(image, x, y, radius):
    # Draw a black circle mask
    mask = np.zeros_like(image)
    cv2.circle(mask, (x, y), radius, (255, 255, 255), -1)

    # Apply the mask to the image
    masked_image = cv2.bitwise_and(image, mask)

    return masked_image

def main():
    # Create the output directory if it doesn't exist
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate over all jpg files in the current directory
    for filename in os.listdir('.'):
        if filename.endswith('.jpg'):
            # Load the image
            image = cv2.imread(filename)

            # Find the sun
            sun_info = find_sun(image)

            if sun_info is not None:
                # Unpack sun coordinates and radius
                x, y, radius = sun_info

                # Create eclipse effect
                eclipse_image = create_eclipse(image, x, y, radius)

                # Save the resulting image in the output directory
                output_path = os.path.join(output_dir, filename)
                cv2.imwrite(output_path, eclipse_image)

                print(f"Eclipse image generated for {filename}.")
            else:
                print(f"Sun not found in {filename}.")

if __name__ == "__main__":
    main()
