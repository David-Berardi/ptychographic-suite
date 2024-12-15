import cv2
import matplotlib.pyplot as plt
import numba as nb
import numpy as np
import pandas as pd


@nb.njit
# Fourier Transform functions with pyfftw
def fft2c(x):
    """
    Perform a centered 2D Fourier transform using pyfftw.
    """
    return np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(x)))


@nb.njit
def ifft2c(x):
    """
    Perform a centered 2D inverse Fourier transform using pyfftw.
    """
    return np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(x)))


# Create a Gaussian probe
def create_gaussian_probe(shape, beam_diameter, wavelength, pixel_size, distance):
    """
    Create a Gaussian probe field based on beam parameters.
    :param shape: Shape of the computational grid (image dimensions).
    :param beam_diameter: Beam diameter at the target plane (in micrometers).
    :param wavelength: Wavelength of the beam (in micrometers).
    :param pixel_size: Size of each sensor pixel (in micrometers).
    :param distance: Distance from the target to the sensor plane (in micrometers).
    :return: Gaussian probe field (2D array).
    """
    beam_waist = beam_diameter / 2.0  # Beam waist (radius)
    k = 2 * np.pi / wavelength  # Wavenumber
    z_R = np.pi * beam_waist**2 / wavelength  # Rayleigh range

    # Spot size at the sensor plane
    spot_size_at_sensor = beam_waist * np.sqrt(1 + (distance / z_R) ** 2)

    # Create a spatial grid
    y = np.arange(-shape[0] // 2, shape[0] // 2) * pixel_size
    x = np.arange(-shape[1] // 2, shape[1] // 2) * pixel_size
    X, Y = np.meshgrid(x, y)

    # Gaussian intensity profile
    probe = np.exp(-(X**2 + Y**2) / (2 * (spot_size_at_sensor / 2.0) ** 2))
    return probe


# Load diffraction patterns and positions
def load_data(image_folder, positions_file, image_indices, pixel_size):
    """
    Load diffraction patterns and convert positions from micrometers to pixel indices.
    :param image_folder: Path to folder containing diffraction images.
    :param positions_file: Path to CSV file with probe positions in micrometers.
    :param image_indices: List of indices for the images.
    :param pixel_size: Sensor pixel size in micrometers.
    :return: List of diffraction patterns, array of positions (in pixels).
    """
    # Load positions from CSV file (in micrometers)
    positions_um = pd.read_csv(positions_file, header=None).values

    # Convert positions to pixel indices
    positions_px = positions_um / pixel_size

    # Load images
    patterns = []
    for i in image_indices:
        image_path = f"{image_folder}/image_{i}.png"
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED).astype(np.float32)
        # print(f"Loading image #{i-1}, shape {image.shape}")
        image /= 65535.0  # Normalize 16-bit images to [0, 1]
        patterns.append(image)

    return patterns, positions_px


def ptychographic_iterative_engine(
    diffraction_patterns, positions_px, pixel_size, probe, iterations=100, beta=0.9
):
    """
    Perform phase retrieval using the Ptychographic Iterative Engine (PIE).
    :param diffraction_patterns: List of measured diffraction patterns.
    :param positions_px: Array of probe positions in pixels (converted from micrometers).
    :param pixel_size: Size of each pixel in micrometers.
    :param probe: Initial probe field (Gaussian).
    :param iterations: Number of iterations for PIE.
    :param beta: Feedback parameter for object update.
    :return: Reconstructed object and probe.
    """
    grid_shape = diffraction_patterns[0].shape

    # Better initial object field: use the average of the diffraction patterns as an initial guess
    initial_object = np.mean(diffraction_patterns, axis=0)

    # Initialize object field with the average diffraction pattern
    object_field = np.sqrt(initial_object) * np.exp(1j * np.angle(initial_object))

    for it in range(iterations):
        print(f"Iteration #{it}")
        for idx, pattern in enumerate(diffraction_patterns):
            print(f"idx: {idx}")
            # Extract the probe position (already in pixels)
            x_pos, y_pos = positions_px[idx]

            # Convert the positions to integer pixel indices
            x_pos, y_pos = int(round(x_pos)), int(round(y_pos))

            # Calculate region of interest (ROI) in the object field
            x_start, x_end = x_pos, x_pos + probe.shape[1]
            y_start, y_end = y_pos, y_pos + probe.shape[0]

            # Ensure the indices are within the image grid size
            x_start, x_end = max(0, x_start), min(grid_shape[1], x_end)
            y_start, y_end = max(0, y_start), min(grid_shape[0], y_end)

            # Get the corresponding region of the object
            object_roi = object_field[y_start:y_end, x_start:x_end]

            # Resize the probe to match the size of the ROI (object field)
            probe_resized = cv2.resize(
                probe, (object_roi.shape[1], object_roi.shape[0])
            )

            # Compute the exit wave (object * probe)
            exit_wave = object_roi * probe_resized

            # Fourier transform of the exit wave
            predicted_pattern = fft2c(exit_wave)

            # Enforce the measured intensity while preserving the phase
            measured_pattern = np.sqrt(pattern)  # Assumption: intensity is measured

            # Resize the diffraction pattern to match the predicted pattern
            if measured_pattern.shape != predicted_pattern.shape:
                measured_pattern = cv2.resize(
                    measured_pattern,
                    (predicted_pattern.shape[1], predicted_pattern.shape[0]),
                )

            updated_pattern = measured_pattern * np.exp(
                1j * np.angle(predicted_pattern)
            )

            # Inverse Fourier transform to get the updated exit wave
            updated_exit_wave = ifft2c(updated_pattern)

            # Update object field with PIE feedback rule
            object_field[y_start:y_end, x_start:x_end] += (
                beta
                * probe_resized.conj()
                * (updated_exit_wave - exit_wave)
                / (np.abs(probe_resized) ** 2 + 1e-8)
            )

        # Optionally display intermediate results
        if it % 10 == 0:
            plt.figure(figsize=(12, 6))
            plt.subplot(1, 2, 1)
            plt.imshow(np.abs(object_field), cmap="gray")
            plt.title(f"Object Magnitude (Iteration {it+1})")
            plt.colorbar()
            plt.subplot(1, 2, 2)
            plt.imshow(np.angle(object_field), cmap="gray")
            plt.title(f"Object Phase (Iteration {it+1})")
            plt.colorbar()
            plt.show()

    return object_field, probe


# Parameters
image_folder = "./images"  # Path to folder containing diffraction patterns
positions_file = "./coordinates.csv"  # Path to CSV file with probe positions
image_indices = range(2, 10)  # Image indices (2 to 201)
pixel_size = 5.5  # Sensor pixel size in micrometers
wavelength = 0.739  # Wavelength in micrometers
probe_diameter = 150  # Beam diameter in micrometers
distance = 69.54 * 1000.0  # Distance in micrometers
iterations = 100  # Number of iterations for PIE
beta = 0.9  # Feedback parameter

# Load data
diffraction_patterns, positions_px = load_data(
    image_folder, positions_file, image_indices, pixel_size
)

# Initialize Gaussian probe
probe = create_gaussian_probe(
    diffraction_patterns[0].shape, probe_diameter, wavelength, pixel_size, distance
)

# Run PIE
reconstructed_object, reconstructed_probe = ptychographic_iterative_engine(
    diffraction_patterns,
    positions_px,
    pixel_size,
    probe,
    iterations=iterations,
    beta=beta,
)

# Display final results
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.imshow(np.abs(reconstructed_object), cmap="gray")
plt.title("Reconstructed Object Magnitude")
plt.colorbar()

plt.subplot(1, 2, 2)
plt.imshow(np.angle(reconstructed_object), cmap="gray")
plt.title("Reconstructed Object Phase")
plt.colorbar()
plt.show()
