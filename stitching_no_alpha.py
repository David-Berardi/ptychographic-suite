import cv2
import numpy as np
from numpy.fft import fft2, fftshift


def generate_grayscale_white_noise_image(size=(500, 500)):
    """
    Generate a grayscale white noise image on demand.
    """

    original_image = np.zeros(size, dtype=np.uint8)
    original_image[48:100, 48:100] = 1  # Simple square as the object
    return np.abs(fftshift(fft2(original_image)))


def vogel_spiral_coordinates(num_points, scale=100):
    """
    Generate real Vogel's spiral coordinates for a given number of points.
    """
    golden_angle_rad = np.pi * (3 - np.sqrt(5))
    indices = np.arange(num_points)
    r = scale * np.sqrt(indices)
    theta = indices * golden_angle_rad
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return np.column_stack((x, y))


def stitch_images_at_coordinates(
    coordinates, image_size=(500, 500), scale_down_factor=1
):
    """
    Stitches images at specified coordinates, blending overlapping regions
    using a weighted average. Images are generated on demand.
    """
    img_h, img_w = (
        image_size[0] // scale_down_factor,
        image_size[1] // scale_down_factor,
    )

    margin = 1  # pixels

    # Determine bounding box for final canvas
    coords_x, coords_y = coordinates[:, 0], coordinates[:, 1]
    min_x, max_x = coords_x.min() - img_w // 2, coords_x.max() + img_w // 2
    min_y, max_y = coords_y.min() - img_h // 2, coords_y.max() + img_h // 2

    # Final canvas size
    canvas_w = int(np.ceil(max_x - min_x)) + margin
    canvas_h = int(np.ceil(max_y - min_y)) + margin

    # Initialize stitched image and weight mask
    stitched_image = np.zeros((canvas_h, canvas_w), dtype=np.uint32)
    weight_mask = np.zeros((canvas_h, canvas_w), dtype=np.uint16)

    # Loop through each image, generate it on demand and place it on the canvas
    for _, (x_center, y_center) in enumerate(coordinates):
        x_center = int(x_center - min_x + margin / 2)
        y_center = int(y_center - min_y + margin / 2)

        # Generate the image on demand and scale down if needed
        img = generate_grayscale_white_noise_image(image_size)
        if scale_down_factor > 1:
            img = cv2.resize(img, (img_w, img_h), interpolation=cv2.INTER_AREA)

        top_left_x = x_center - img_w // 2
        top_left_y = y_center - img_h // 2

        # Get the region where the image will be placed
        stitched_roi = stitched_image[
            top_left_y : top_left_y + img_h, top_left_x : top_left_x + img_w
        ]
        weight_roi = weight_mask[
            top_left_y : top_left_y + img_h, top_left_x : top_left_x + img_w
        ]

        # Update the stitched image with weighted blending (adding)
        np.add(stitched_roi, img.astype(np.uint32), out=stitched_roi)
        np.add(weight_roi, 1, out=weight_roi)

    # Normalize the stitched image by the weight mask
    valid_mask = weight_mask > 0
    stitched_image[valid_mask] = stitched_image[valid_mask] // weight_mask[valid_mask]
    stitched_image = np.clip(stitched_image, 0, 255).astype(np.uint8)

    return stitched_image


# Settings
num_images = 119
image_size = (500, 500)
scale_down_factor = 1  # Scale down the image for final resolution (e.g., 2x)

# Get Vogel's spiral coordinates
coordinates = vogel_spiral_coordinates(num_images, scale=1)

# Stitch the generated images together at the spiral coordinates
stitched_image = stitch_images_at_coordinates(
    coordinates, image_size, scale_down_factor
)

# Save the final stitched image
output_filename = "stitched_image_3.png"
cv2.imwrite(output_filename, stitched_image)

# Display the result
cv2.imshow("Stitched Image", stitched_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
