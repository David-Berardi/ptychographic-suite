import cv2
import numpy as np
import pandas as pd

# Constants
WAVELENGTH = 739e-9  # Wavelength in meters (739 nm)
DISTANCE = 68.54e-3  # Distance between target and sensor in meters (68.54 mm)
PROBE_DIAMETER = 150e-6  # Probe diameter in meters (150 µm)
PIXEL_SIZE = 5.5e-6  # Sensor pixel size in meters (5.5 µm)

# Compute scaling factor
SCALING_FACTOR = (WAVELENGTH * DISTANCE) / PROBE_DIAMETER


def read_coordinates(csv_file):
    """Read target-plane coordinates (in micrometers) from a CSV file using pandas."""
    df = pd.read_csv(csv_file)  # Using pandas to read the CSV
    coordinates = df[["x", "y"]].values  # Assuming the columns are named 'x' and 'y'
    return coordinates


def map_to_sensor_plane(x_target, y_target):
    """Map target-plane coordinates (in micrometers) to sensor-plane coordinates (in meters)."""
    # Convert micrometers to meters
    x_sensor = SCALING_FACTOR * x_target * 1e-6  # Convert x from µm to meters
    y_sensor = SCALING_FACTOR * y_target * 1e-6  # Convert y from µm to meters
    return x_sensor, y_sensor


def sensor_coordinates_to_pixels(x_sensor, y_sensor, pixel_size):
    """Convert sensor-plane coordinates (in meters) to pixel indices."""
    x_pixel = int(round(x_sensor / pixel_size))  # Convert from meters to pixel index
    y_pixel = int(round(y_sensor / pixel_size))  # Convert from meters to pixel index
    return x_pixel, y_pixel


def stitch_images(
    image_folder, coordinates_csv, output_path, canvas_width, canvas_height
):
    """Stitch diffraction pattern images based on probe coordinates."""
    # Read coordinates from CSV
    coordinates = read_coordinates(coordinates_csv)

    # Initialize the canvas
    canvas = np.zeros((canvas_height, canvas_width), dtype=np.float32)
    count_canvas = np.zeros_like(canvas)  # To count overlaps

    for idx, (x_target, y_target) in enumerate(coordinates, start=2):
        print(f"idx: {idx}")
        # Start from image 2
        # Map target-plane coordinates (in micrometers) to sensor-plane coordinates (in meters)
        x_sensor, y_sensor = map_to_sensor_plane(x_target, y_target)

        # Convert sensor-plane coordinates to pixel indices
        x_pixel, y_pixel = sensor_coordinates_to_pixels(x_sensor, y_sensor, PIXEL_SIZE)

        # Load the diffraction pattern image
        image_path = f"{image_folder}/converted_{idx}.png"  # Image name pattern
        image = (
            cv2.imread(image_path, cv2.IMREAD_ANYDEPTH).astype(np.float64) / 65535.0
        )  # Normalize

        # Determine the placement on the canvas
        h, w = image.shape
        x_start = max(x_pixel - w // 2, 0)
        x_end = min(x_start + w, canvas_width)
        y_start = max(y_pixel - h // 2, 0)
        y_end = min(y_start + h, canvas_height)

        # Add the image to the canvas
        canvas[y_start:y_end, x_start:x_end] += image[
            : y_end - y_start, : x_end - x_start
        ]
        count_canvas[y_start:y_end, x_start:x_end] += 1

    # Normalize overlapping regions
    count_canvas[count_canvas == 0] = 1  # Avoid division by zero
    stitched_image = canvas / count_canvas

    # Save the stitched result
    stitched_image = (stitched_image * 65535).astype(
        np.uint16
    )  # Convert back to 16-bit
    cv2.imwrite(output_path, stitched_image)
    print(f"Stitched image saved to {output_path}")


# Example usage
if __name__ == "__main__":
    image_folder = "converted"  # Folder containing the diffraction images
    coordinates_csv = "coordinates.csv"  # CSV file with target-plane coordinates
    output_path = "converted_corrected_stitch.png"  # Output file for the stitched image
    canvas_width, canvas_height = 5000, 5000  # Adjust canvas size as needed
    stitch_images(
        image_folder, coordinates_csv, output_path, canvas_width, canvas_height
    )
