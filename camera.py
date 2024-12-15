import os

import cv2
import imutils  # type: ignore
import numpy as np
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage

from tl_dotnet_wrapper import TL_SDK

# TODO: fix slow update rate of GUI -> maybe use camera.queue and/or don't display/emit 1 out of N frames


# NOTE: The frames received from the camera are 16 bit !!!
class ScientificCamera(QThread):
    # Emit signal with processed frame/s,
    frame_signal = Signal(QImage)
    model_signal = Signal(str)
    written_signal = Signal(bool)

    debug = 2
    stop = False

    exposure_flag = False
    gain_flag = False
    bins_flag = False

    def __init__(self, n_frames=1, exposure_ms=1, gain=25, bins=1):
        super().__init__()
        self.n_frames = n_frames
        self.exposure_ms = exposure_ms
        self.gain = gain
        self.bins = bins

    def run(self):
        if self.debug == 0:
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

        elif self.debug == 1:
            # continuous frame polling
            try:
                # initialize camera sdk
                sdk = TL_SDK()
                available_cameras = sdk.get_camera_list()

                # NOTE: dispose of SDK if nothing works, otherwise it remains open!!!

                # Return if no cameras detected
                if len(available_cameras) < 1:
                    print("no cameras detected")
                    sdk.close()
                    return

                # open camera
                camera = sdk.open_camera(available_cameras[0])

                # default parameters
                camera.set_exposure_time_us(self.exposure_ms * 1000)  # ms
                camera.set_frames_per_trigger_zero_for_unlimited(0)  # continuous mode

                # TODO: set gain

                # TODO: set taps
                # camera.set_taps(4)

                # set data rate
                # camera.set_data_rate("30FPS")

                # set frame rate control
                camera.set_is_frame_rate_controlled(True)
                camera.set_frame_rate_fps(15)

                # TODO: set image queue in order to speed up process
                # NOTE: too slow when immediately retrieving frame instead of queueing frames!
                # camera.set_maximum_number_of_frames_to_queue(10)

                # emit camera model
                self.model_signal.emit(camera.get_model())

                # arm camera and set to software trigger
                camera.arm()
                camera.issue_software_trigger()

                self.is_captured = False
                index = 0
                imaging_index = 1
                frames = []

                while True:
                    # stop camera
                    if self.stop:
                        break

                    # update exposure before getting pending frame
                    if self.exposure_flag:
                        camera.set_exposure_time_us(self.exposure_ms * 1000)
                        self.exposure_flag = False

                    # actual polling for single frame
                    frame = None
                    while frame is None:
                        frame = camera.get_pending_frame_or_null()

                    # TODO: use pending_ARRAY and return each frame in array

                    if frame is not None:
                        # NOTE: using grayscale instead of RGB
                        # save current frame
                        frame = camera.frame_to_array(frame)

                        # capture N frames
                        if self.is_captured:
                            frames.append(frame)
                            index += 1
                            print(f"Frame #{imaging_index}")

                            # take average of N frames
                            if index == self.n_frames:
                                final_image = np.array(
                                    np.mean(frames, axis=(0)), dtype=np.uint16
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

                                index = 0
                                imaging_index += 1
                                frames = []
                                self.is_captured = False

                        # resize and convert frame to QImage and emit it
                        # TODO: decouple conversion into MainWindow, just emit the numpy array
                        # NOTE: since it's grayscale, no need to create 3 dimensional array for RGB
                        # DON'T RESIZE
                        # frame = imutils.resize(frame, width=240, height=240)

                        image = QImage(
                            frame,
                            frame.shape[1],
                            frame.shape[0],
                            QImage.Format_Grayscale16,
                        )
                        self.frame_signal.emit(image)

                    else:
                        # print("Unable to acquire image")
                        continue

                # don't close the camera and sdk each time, insted grab image whenever requested
                # make sure to disarm each time an image is grabbed
                camera.disarm()
                camera.close()
                sdk.close()

            except Exception as error:
                print(f"Error: {error}")
                sdk.close()
                return
        else:
            # single frame
            try:
                # initialize camera sdk
                sdk = TL_SDK()
                available_cameras = sdk.get_camera_list()

                # NOTE: dispose of SDK if nothing works, otherwise it remains open!!!
                # Return if no cameras detected
                if len(available_cameras) < 1:
                    print("no camera detected")
                    sdk.close()
                    return

                # open camera
                camera = sdk.open_camera(available_cameras[0])

                # emit camera model
                self.model_signal.emit(camera.get_model())

                # set frames per trigger to single capture
                camera.set_frames_per_trigger_zero_for_unlimited(1)

                # default parameters
                # set exposure, gain, black level
                camera.set_black_level(54)
                camera.set_exposure_time_us(self.exposure_ms * 1000)
                camera.set_gain(self.gain)

                # set binning to (0, 0), w: 3296, h: 2472, binx = biny
                print(
                    f"width: {camera.get_sensor_width_pixels()}, height: {camera.get_sensor_height_pixels()}"
                )
                camera.set_roi_binning(
                    0,
                    0,
                    camera.get_sensor_width_pixels(),
                    camera.get_sensor_height_pixels(),
                    self.bins,
                    self.bins,
                )

                self.is_captured = False
                index = 0
                imaging_index = 1
                frames = []

                while True:
                    # stop camera
                    if self.stop:
                        break

                    # update exposure
                    if self.exposure_flag:
                        camera.set_exposure_time_us(self.exposure_ms * 1000)
                        self.exposure_flag = False

                    # update gain
                    if self.gain_flag:
                        camera.set_gain(self.gain)
                        self.gain_flag = False

                    # NOTE: to set the ROI, camera must be disarmed
                    # update bins (w: 3296, h: 2472)
                    if self.bins_flag:
                        camera.set_roi_binning(
                            0,
                            0,
                            camera.get_sensor_width_pixels(),
                            camera.get_sensor_height_pixels(),
                            self.bins,
                            self.bins,
                        )
                        self.bins_flag = False

                    # capture N frames
                    if self.is_captured:
                        # call disarm before arming to clear current queue
                        camera.disarm()

                        # TODO: check if you need to set exposure and gain at each trigger
                        print(
                            f"Before, exposure: {camera.get_exposure_time_us()*1000}, gain: {camera.get_gain()}"
                        )

                        # TODO: read manual and check if set_frames_per_trigger is to be called each time to capture
                        # camera.set_exposure_time_us(self.exposure_ms * 1000)
                        # camera.set_gain(self.gain)
                        # camera.set_frames_per_trigger_zero_for_unlimited(1)
                        # camera.set_maximum_number_of_frames_to_queue(10)

                        camera.arm()
                        camera.issue_software_trigger()

                        # TODO
                        print(
                            f"After, exposure: {camera.get_exposure_time_us()*1000}, gain: {camera.get_gain()}"
                        )

                        # actual polling for single frame
                        frame = None
                        while frame is None:
                            frame = camera.get_pending_frame_or_null()

                        # convert frame to numpy.array
                        # NOTE: using grayscale instead of RGB
                        frame = camera.frame_to_array(frame)

                        frames.append(frame)
                        index += 1
                        print(f"Frame #{imaging_index}")

                        # take average of N frames
                        # NOTE: np.uint16 !!!
                        if index == self.n_frames:
                            if self.n_frames > 1:
                                final_image = np.array(
                                    np.mean(frames, axis=(0)), dtype=np.uint16
                                )

                                # NOTE: returns true if the image was successfully written
                                written = cv2.imwrite(
                                    os.path.join(
                                        self.directory,
                                        f"image_{imaging_index}.png",
                                    ),
                                    final_image,
                                )
                            else:
                                written = cv2.imwrite(
                                    os.path.join(
                                        self.directory,
                                        f"image_{imaging_index}.png",
                                    ),
                                    frame,
                                )

                            # send signal for written and bind it to ptychography module
                            self.written_signal.emit(written)

                            index = 0
                            imaging_index += 1
                            frames = []
                            self.is_captured = False

                            # NOTE: remember to disarm camera each time
                            camera.disarm()

                        # resize and convert frame to QImage and emit it
                        # TODO: decouple conversion into MainWindow, just emit the numpy array
                        # NOTE: since it's grayscale, no need to create 3 dimensional array for RGB
                        # don't resize
                        # frame = imutils.resize(frame, width=600, height=600)

                        image = QImage(
                            frame,
                            frame.shape[1],
                            frame.shape[0],
                            QImage.Format_Grayscale16,
                        )
                        self.frame_signal.emit(image)

                # don't close the camera and sdk each time, instead grab image whenever requested
                # make sure to disarm each time an image is grabbed
                camera.disarm()
                camera.close()
                sdk.close()

            except Exception as error:
                print(f"Error: {error}")
                sdk.close()
                return

    def cvimage_to_label(self, image):
        image = imutils.resize(image, width=240, height=240)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(image, image.shape[1], image.shape[0], QImage.Format_RGB888)
        return image

    def update_exposure(self, exposure_ms):
        self.exposure_flag = True
        self.exposure_ms = exposure_ms

    def update_gain(self, gain):
        self.gain_flag = True
        self.gain = gain

    def update_bins(self, bins):
        self.bins_flag = True
        self.bins = bins

    def capture(self, directory, n_frames):
        self.is_captured = True
        self.n_frames = n_frames
        self.directory = directory
