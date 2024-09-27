#!/usr/bin/python3
import sys
import time

import cv2
import imutils
import numpy as np
import smaract.ctl as ctl
from PySide6.QtCore import QObject, QThread, QTimer, Signal, Slot
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QDialog, QMainWindow

# if on Windows, use the provided setup script to add the DLLs folder to the PATH
""" from windows_setup import configure_path

configure_path() """

import queue
import threading

from PIL import Image

from form_dialog_ui import Ui_Dialog
from main_window_ui import Ui_MainWindow

# from thorlabs_tsi_sdk.tl_camera import Frame, TLCamera, TLCameraSDK


class Signals(QObject):
    error = Signal(str)
    locator = Signal(str)
    update_data = Signal(list)
    pos = Signal(int)


class MCS2_Controller:
    def __init__(self):
        self.signals = Signals()
        self.d_handle = None

    # TODO: add group actions for multiple channels
    # TODO: implement velocity, acceleration, etc. settings through gui
    def initialize_controller(self):
        # setup timer for data polling
        self.timer = QTimer()
        self.timer.setInterval(750)  # ms
        self.timer.timeout.connect(self.update_data)

        # self.timer.start()

        # self.signals.error.emit("alpha")
        # check version and compability
        print("*******************************************************")
        print("*               SmarAct MCS2 Controller               *")
        print("*******************************************************")

        version = ctl.GetFullVersionString()
        print(f"SmarActCTL library version: '{version}'.")
        self.assert_lib_compatibility()

        # Find available MCS2 devices
        try:
            buffer = ctl.FindDevices()

            if len(buffer) == 0:
                self.signals.error.emit("MCS2 no devices found.")
                print("MCS2 no devices found.")
                return

            locators = buffer.split("\n")
            for locator in locators:
                self.signals.locator.emit(locator)
                print(f"MCS2 available devices: {locator}")

            # Controller Handle
            self.d_handle = ctl.Open(locator)

            base_unit = ctl.GetProperty_i32(
                self.d_handle, 0, ctl.Property.POS_BASE_UNIT
            )

            position = ctl.GetProperty_i64(self.d_handle, 0, ctl.Property.POSITION)
            self.signals.pos.emit(position)
            print(f"MCS2 position of channel {0}: {position}", end="")
            print("pm.") if base_unit == ctl.BaseUnit.METER else print("ndeg.")

            # default velocity for all channels [in pm/s]
            ctl.SetProperty_i64(
                self.d_handle, 0, ctl.Property.MOVE_VELOCITY, 1000000000
            )
            ctl.SetProperty_i64(
                self.d_handle, 1, ctl.Property.MOVE_VELOCITY, 1000000000
            )
            ctl.SetProperty_i64(
                self.d_handle, 2, ctl.Property.MOVE_VELOCITY, 1000000000
            )

            # default acceleration for all channels [in pm/s2]
            ctl.SetProperty_i64(
                self.d_handle, 0, ctl.Property.MOVE_ACCELERATION, 1000000000
            )
            ctl.SetProperty_i64(
                self.d_handle, 1, ctl.Property.MOVE_ACCELERATION, 1000000000
            )
            ctl.SetProperty_i64(
                self.d_handle, 2, ctl.Property.MOVE_ACCELERATION, 1000000000
            )

            # start data acquisition
            self.timer.start()

        except Exception as e:
            self.signals.error.emit("MCS2 failed to find devices. Exit.")
            print("MCS2 failed to find devices. Exit.")
            return

    def assert_lib_compatibility(self):
        vapi = ctl.api_version
        vlib = [int(i) for i in ctl.GetFullVersionString().split(".")]
        if vapi[0] != vlib[0]:
            raise RuntimeError(
                "Incompatible SmarActCTL python api and library version."
            )

    @Slot(int)
    def set_movement_mode(self, mode):
        if mode == 0:
            # TODO: write as command group
            ctl.SetProperty_i32(
                self.d_handle, 0, ctl.Property.MOVE_MODE, ctl.MoveMode.CL_ABSOLUTE
            )
            ctl.SetProperty_i32(
                self.d_handle, 1, ctl.Property.MOVE_MODE, ctl.MoveMode.CL_ABSOLUTE
            )
            ctl.SetProperty_i32(
                self.d_handle, 2, ctl.Property.MOVE_MODE, ctl.MoveMode.CL_ABSOLUTE
            )
            print(
                f"Movement Mode: {ctl.GetProperty_i32(self.d_handle, 0, ctl.Property.MOVE_MODE)} ABSOLUTE"
            )
        if mode == 1:
            # TODO: write as command group
            ctl.SetProperty_i32(
                self.d_handle, 0, ctl.Property.MOVE_MODE, ctl.MoveMode.CL_RELATIVE
            )
            ctl.SetProperty_i32(
                self.d_handle, 1, ctl.Property.MOVE_MODE, ctl.MoveMode.CL_RELATIVE
            )
            ctl.SetProperty_i32(
                self.d_handle, 2, ctl.Property.MOVE_MODE, ctl.MoveMode.CL_RELATIVE
            )
            print(
                f"Movement Mode: {ctl.GetProperty_i32(self.d_handle, 0, ctl.Property.MOVE_MODE)} RELATIVE"
            )

    @Slot()
    def reference(self):
        # TODO: write as command group
        ctl.SetProperty_i32(self.d_handle, 0, ctl.Property.REFERENCING_OPTIONS, 0)

        # Set velocity to 1mm/s
        ctl.SetProperty_i64(self.d_handle, 0, ctl.Property.MOVE_VELOCITY, 1000000000)
        # Set acceleration to 10mm/s2.
        ctl.SetProperty_i64(
            self.d_handle, 0, ctl.Property.MOVE_ACCELERATION, 10000000000
        )
        # Start referencing sequence
        ctl.Reference(self.d_handle, 0)
        position = ctl.GetProperty_i64(self.d_handle, 0, ctl.Property.POSITION)
        self.signals.pos.emit(position)

    # TODO: set position to zero after referencing

    @Slot()
    def calibrate(self):
        # TODO: write as command group
        ctl.SetProperty_i32(self.d_handle, 0, ctl.Property.CALIBRATION_OPTIONS, 0)
        ctl.SetProperty_i32(self.d_handle, 1, ctl.Property.CALIBRATION_OPTIONS, 0)
        ctl.SetProperty_i32(self.d_handle, 2, ctl.Property.CALIBRATION_OPTIONS, 0)

        # Start calibration sequence
        ctl.Calibrate(self.d_handle, 0)

        # TODO: write as command group
        position_x = ctl.GetProperty_i64(self.d_handle, 0, ctl.Property.POSITION)
        position_y = ctl.GetProperty_i64(self.d_handle, 1, ctl.Property.POSITION)
        position_z = ctl.GetProperty_i64(self.d_handle, 2, ctl.Property.POSITION)

        position = [position_x, position_y, position_z]

        self.signals.update_data.emit(position)

    def move(self, position):
        position_to_pm = position * 1000
        ctl.Move(self.d_handle, 0, position_to_pm, 0)

        print(f"MCS2 move channel {0} to absolute position: {position_to_pm} pm.")

    def abort(self):
        # TODO: write as command group
        ctl.Stop(self.d_handle, 0)
        print("MCS2 stop channel: 0.")

    def update_data(self):
        # TODO: write as command group
        # position_x = ctl.GetProperty_i64(self.d_handle, 0, ctl.Property.POSITION)
        # position_y = ctl.GetProperty_i64(self.d_handle, 1, ctl.Property.POSITION)
        # position_z = ctl.GetProperty_i64(self.d_handle, 2, ctl.Property.POSITION)

        # position = [position_x, position_y, position_z]

        position = [
            np.random.randint(0, 1000000),
            np.random.randint(0, 1000000),
            np.random.randint(0, 1000000),
        ]
        self.signals.update_data.emit(position)


# TODO: create path generator class, for paths creation to feed to the controller


class ScientificCamera(QThread):
    """def __init__(self, camera):
        super().__init__()
        self._camera = camera
        self._previous_timestamp = 0

        self._bit_depth = camera.bit_depth
        self._camera.image_poll_timeout_ms = (
            0  # Do not want to block for long periods of time
        )
        self._image_queue = queue.Queue(maxsize=2)

    def get_output_queue(self):
        return self._image_queue

    def _get_image(self, frame):
        # no coloring, just scale down image to 8 bpp and place into PIL Image object
        scaled_image = frame.image_buffer >> (self._bit_depth - 8)
        return Image.fromarray(scaled_image)

    # TODO: convert image to QPixmap and display in place of the "live view" label
    def run(self):
        while True:
            try:
                frame = self._camera.get_pending_frame_or_null()
                if frame is not None:
                    if self._is_color:
                        pil_image = self._get_color_image(frame)
                    else:
                        pil_image = self._get_image(frame)
                    self._image_queue.put_nowait(pil_image)
            except queue.Full:
                # queue full
                pass
            except Exception as error:
                print(f"Encountered error: {error}, image acquisition will stop.")
                break
        print("Image acquisition has stopped")"""

    frame_signal = Signal(QImage)

    def run(self):
        self.is_captured = False
        self.cap = cv2.VideoCapture(0)

        while self.cap.isOpened():
            # cv2.waitKey(15)  # fps
            _, frame = self.cap.read()

            if self.is_captured:
                cv2.imwrite("D:/Downloads/frame_image.png", frame)
                self.is_captured = False

            frame = self.cvimage_to_label(frame)
            self.frame_signal.emit(frame)

    def cvimage_to_label(self, image):
        image = imutils.resize(image, width=240, height=240)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(image, image.shape[1], image.shape[0], QImage.Format_RGB888)
        return image

    def capture(self):
        self.is_captured = True


class MoveForm(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


# TODO: add commands for incremental steps of the linear stages
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # controller
        self.refresh_button.clicked.connect(self.refresh_controller)
        self.move_button.clicked.connect(self.create_form)

        # TODO: for testing, move to show_locator
        self.move_button.setEnabled(True)

        # camera
        self.refresh_camera_button.clicked.connect(self.refresh_camera)
        self.camera_thread = ScientificCamera()
        self.camera_thread.frame_signal.connect(self.setImage)
        self.capture_button.clicked.connect(self.camera_thread.capture)

    def refresh_controller(self):
        if self.devices.count() == 0:
            self.device = MCS2_Controller()

            self.device.signals.error.connect(self.show_error)
            self.device.signals.locator.connect(self.show_locator)
            self.device.signals.update_data.connect(self.get_position)

            self.device.initialize_controller()

    def refresh_camera(self):
        """if self.cameras.count() == 0:
        self.camera = ScientificCamera()"""
        self.camera_thread.start()

    @Slot(QImage)
    def setImage(self, image):
        self.live_feed.setPixmap(QPixmap.fromImage(image))

    @Slot(str)
    def show_error(self, error_message):
        self.error_label.setText(error_message)

    @Slot(str)
    def show_locator(self, locator_id):
        self.devices.addItem(f"Device {locator_id}")
        self.devices.setCurrentIndex(0)

        # re-enable buttons and make fields visible
        self.position_0.setEnabled(True)
        self.position_1.setEnabled(True)
        self.velocity_0.setEnabled(True)
        self.velocity_1.setEnabled(True)
        self.acceleration_0.setEnabled(True)
        self.acceleration_1.setEnabled(True)
        self.move_mode_select.setEnabled(True)
        self.move_mode_label.setEnabled(True)
        self.reference_button.setEnabled(True)
        self.calibrate_button.setEnabled(True)
        self.move_button.setEnabled(True)

        # add movement modes
        self.move_mode_select.addItem("Absolute Mode")
        self.move_mode_select.addItem("Relative Mode")

        self.move_mode_select.currentIndexChanged.connect(self.device.set_movement_mode)

        # add functionality to reference and calibrate buttons
        # TODO: setup image acquisition
        self.reference_button.clicked.connect(self.device.reference)
        self.calibrate_button.clicked.connect(self.device.calibrate)

    def create_form(self):
        self.move_form = MoveForm()

        self.move_form.move_button.clicked.connect(self.move)
        self.move_form.abort_button.clicked.connect(self.device.abort)

        if self.move_form.exec():
            print("Movement Form")

    def move(self):
        # add movement functionality
        print(self.move_form.position_0.value())
        self.device.move(int(self.move_form.position_0.value()))

    @Slot(list)
    def get_position(self, position):
        self.position_0.setValue(position[0])
        self.position_1.setValue(position[1])
        self.position_2.setValue(position[2])


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()
