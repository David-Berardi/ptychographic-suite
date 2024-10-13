#!/usr/bin/python3
import os
import sys

from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QDialog, QFileDialog, QMainWindow

from camera import ScientificCamera
from controller import MCS2_Controller
from form_dialog_ui import Ui_Dialog
from main_window_ui import Ui_MainWindow
from ptychography import Ptychography


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

    def refresh_controller(self):
        if self.devices.count() == 0:
            self.device = MCS2_Controller()

            self.device.signals.error.connect(self.show_error)
            self.device.signals.locator.connect(self.show_locator)
            self.device.signals.update_data.connect(self.get_position)
            self.device.signals.default.connect(self.default)

            self.device.initialize_controller()

    def refresh_camera(self):
        if self.cameras.count() == 0:
            self.camera = ScientificCamera()
            self.camera.start()

            self.directory_label.setText(str(os.getcwd()))

            self.camera.frame_signal.connect(self.setImage)
            self.camera.model_signal.connect(self.show_model)
            self.capture_button.clicked.connect(self.capture)
            self.exposure.valueChanged.connect(self.update_exposure)
            self.directory_button.clicked.connect(self.select_directory)
            self.stop_button.clicked.connect(self.stop_camera)

    @Slot(str)
    def show_model(self, model):
        self.cameras.addItem(f"Camera {str(model)}")
        self.cameras.setCurrentIndex(0)

    @Slot(list)
    def default(self, settings):
        print(settings)
        self.velocity_0.setValue(settings[0])
        self.velocity_1.setValue(settings[0])
        self.velocity_2.setValue(settings[0])

        self.acceleration_0.setValue(settings[1])
        self.acceleration_1.setValue(settings[1])
        self.acceleration_2.setValue(settings[1])

    @Slot(QImage)
    def setImage(self, image):
        self.live_feed.setPixmap(QPixmap.fromImage(image))

    @Slot(str)
    def show_error(self, error_message):
        self.error_label.setText(error_message)

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self, caption="Select Directory", options=QFileDialog.Option.ShowDirsOnly
        )
        self.directory_label.setText(directory)

    def capture(self):
        directory = self.directory_label.text()
        frames = self.frames.value()
        self.camera.capture(directory, frames)

    def update_exposure(self):
        print("exposure updated")
        self.camera.update_exposure(self.exposure.value())

    def stop_camera(self):
        self.live_feed.setText("Live Feed")
        self.cameras.removeItem(0)

        self.directory_label.setText("")

        self.capture_button.clicked.disconnect()
        self.directory_button.clicked.disconnect()
        self.stop_button.clicked.disconnect()
        self.exposure.valueChanged.disconnect()

        # Stop camera thread
        self.camera.stop = True
        self.camera.quit()

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
        self.reference_button.clicked.connect(self.device.reference)
        self.calibrate_button.clicked.connect(self.device.calibrate)

    def create_form(self):
        self.move_form = MoveForm()

        self.move_form.move_button.clicked.connect(self.move)
        self.move_form.abort_button.clicked.connect(self.device.abort)

        # current position
        self.move_form.position_0.setValue(self.position_0.value())
        self.move_form.position_1.setValue(self.position_1.value())
        self.move_form.position_2.setValue(self.position_2.value())

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

    # safely close connection to Controller
    # TODO: decouple
    def closeEvent(self, event):
        if self.device.d_handle is not None:
            # ctl.Close(self.device.d_handle)
            pass

        super(QMainWindow, self).closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()
