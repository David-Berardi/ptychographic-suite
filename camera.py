# add the DLLs folder to the PATH
try:
    # if on Windows, use the provided setup script to add the DLLs folder to the PATH
    from windows_setup import configure_path

    configure_path()
except ImportError:
    # configure_path = None
    print("Couldn't load DDLs")

import os

import cv2
import imutils  # type: ignore
import numpy as np
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage
from thorlabs_tsi_sdk.tl_camera import TLCameraSDK  # type: ignore


class ScientificCamera(QThread):
    # Emit signal with processed frame/s,
    frame_signal = Signal(QImage)
    model_signal = Signal(str)
    written_signal = Signal(bool)
    stop = False
    debug = False
    exposure_flag = False

    def run(self):
        if self.debug:
            self.is_captured = False
            self.cap = cv2.VideoCapture(0)

            i = 0
            frames = []
            self.model_signal.emit("Thorcam")

            while self.cap.isOpened():
                _, frame = self.cap.read()

                if self.stop:
                    break

                if self.is_captured:
                    frames.append(frame)
                    i += 1
                    print(f"Frame #{i}")

                    if i == self.frames:
                        final_image = np.array(
                            np.mean(frames, axis=(0)), dtype=np.uint8
                        )
                        written = cv2.imwrite(
                            os.path.join(self.directory, "image_directory.png"),
                            final_image,
                        )

                        self.written_signal.emit(written)

                        i = 0
                        frames = []
                        self.is_captured = False

                frame = self.cvimage_to_label(frame)
                self.frame_signal.emit(frame)

            self.cap.release()
            cv2.destroyAllWindows()

        else:
            # initialize camera sdk
            with TLCameraSDK() as sdk:
                available_cameras = sdk.discover_available_cameras()

                # Return if no cameras detected
                if len(available_cameras) < 1:
                    # self.model_signal.emit("Thorcam")
                    print("no cameras detected")
                    return

                # open camera
                with sdk.open_camera(available_cameras[0]) as camera:
                    # default parameters
                    camera.exposure_time_us = 11000  # 11 ms
                    camera.frames_per_trigger_zero_for_unlimited = 0  # continuous mode
                    camera.image_poll_timeout_ms = 1000  # 1 second polling timeout
                    camera.frame_rate_control_value = 15
                    camera.is_frame_rate_control_enabled = True

                    # emit camera model
                    self.model_signal.emit(camera.model)

                    # arm camera and set to software trigger
                    camera.arm(2)
                    camera.issue_software_trigger()

                    self.is_captured = False
                    index = 0
                    imaging_index = 1
                    frames = []

                    # continuous frame polling
                    try:
                        while True:
                            # stop camera
                            if self.stop:
                                break

                            # update exposure before getting pending frame
                            if self.exposure_flag:
                                camera.exposure_time_us = self.exposure
                                self.exposure_flag = False

                            # actual polling for single frame
                            frame = camera.get_pending_frame_or_null()

                            if frame is not None:
                                print(f"Frame #{frame.frame_count} received!")

                                # save current frame
                                # frame.image_buffer
                                image_buffer_copy = np.copy(frame.image_buffer)

                                # convert to numpy array (3 channels)
                                shaped_frame = image_buffer_copy.reshape(
                                    camera.image_height_pixels,
                                    camera.image_width_pixels,
                                )
                                converted_frame = np.zeros(
                                    (
                                        camera.image_height_pixels,
                                        camera.image_width_pixels,
                                        3,
                                    ),
                                    dtype=np.uint8,
                                )
                                converted_frame[:, :, 0] = shaped_frame
                                converted_frame[:, :, 1] = shaped_frame
                                converted_frame[:, :, 2] = shaped_frame

                                # capture N frames
                                if self.is_captured:
                                    # TODO: since it's in grayscale use "shaped_frame" instead of converted_frame, there's no need of three channels
                                    frames.append(converted_frame)
                                    index += 1
                                    print(f"Frame #{index}")

                                    # take average of N frames
                                    if index == self.frames:
                                        final_image = np.array(
                                            np.mean(frames, axis=(0)), dtype=np.uint8
                                        )

                                        # NOTE: returns true if the image was successfully written
                                        written = cv2.imwrite(
                                            os.path.join(
                                                self.directory,
                                                f"image_{imaging_index}.png",
                                            ),
                                            final_image,
                                        )

                                        # send signal for written and bind it to ptychography module
                                        self.written_signal.emit(written)

                                        i = 0
                                        imaging_index += 1
                                        frames = []
                                        self.is_captured = False

                                # resize and convert frame to QImage and emit it
                                # TODO: decouple conversion into MainWindow, just emit the numpy array
                                frame = imutils.resize(
                                    converted_frame, width=240, height=240
                                )
                                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                frame = QImage(
                                    frame,
                                    frame.shape[1],
                                    frame.shape[0],
                                    QImage.Format_RGB888,
                                )
                                self.frame_signal.emit(frame)

                            else:
                                print("Unable to acquire image")
                                break

                    except Exception as error:
                        print(f"Error: {error}")

                    # disarm camera (optional)
                    camera.disarm()

    def cvimage_to_label(self, image):
        image = imutils.resize(image, width=240, height=240)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(image, image.shape[1], image.shape[0], QImage.Format_RGB888)
        return image

    def update_exposure(self, exposure):
        self.exposure_flag = True
        self.exposure = exposure

    def capture(self, directory, frames):
        self.is_captured = True
        self.frames = frames
        self.directory = directory
