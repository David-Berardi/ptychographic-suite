#!/usr/bin/python3
import os
import sys
from functools import partial

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
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

        # create and configure ptychography module
        self.ptychography = Ptychography()
        self.trajectory_select.addItem("Fermat Spiral")
        self.ptychography.current_coordinate_signal.connect(self.update_point)

        # scatter plot of trajectory
        self.mpl = FigureCanvas(Figure(figsize=(4, 2), tight_layout=True))
        self.acquisition_layout.addWidget(self.mpl)
        self.axes = self.mpl.figure.subplots()
        self.axes.set_xlabel("X plane [nm]")
        self.axes.set_ylabel("Y plane [nm]")
        self.axes.set_title("Fermat Spiral Trajectory")
        self.axes.grid()

        self.trajectory_generate_button.clicked.connect(self.generate_graph)

        # ptychography start
        self.start_trajectory_button.setEnabled(True)
        self.start_trajectory_button.clicked.connect(self.start_acquisition)

        # controller
        self.refresh_button.clicked.connect(self.refresh_controller)
        self.move_button.clicked.connect(self.create_form)

        # TODO: for testing, move to show_locator
        self.move_button.setEnabled(True)

        # camera
        self.refresh_camera_button.clicked.connect(self.refresh_camera)

    def start_acquisition(self):
        if not self.ptychography.isRunning():
            print("Initializing acquisition sequence")

            # TODO: decouple creating method in ptychography
            # set z-stage coordinate, directory, number of frames
            self.ptychography.center_z = self.trajectory_center_z.value()
            self.ptychography.directory = self.directory_label.text()
            self.ptychography.frames = self.frames.value()

            # start acquisition sequence (thread)
            self.ptychography.start()

    def generate_graph(self):
        # clear axis at each generation
        self.axes.cla()
        self.axes.set_xlabel("X plane [nm]")
        self.axes.set_ylabel("Y plane [nm]")
        self.axes.set_title("Fermat Spiral Trajectory")
        self.axes.grid()

        # generate coordinates
        self.ptychography.generate(
            self.trajectory_center_x.value(),
            self.trajectory_center_y.value(),
            self.trajectory_radius.value(),
        )

        # plot coordinates and current point
        self.axes.scatter(
            self.ptychography.coordinates[:, 0], self.ptychography.coordinates[:, 1]
        )
        self.current_coordinate_plot = self.axes.scatter(
            self.ptychography.coordinates[0, 0],
            self.ptychography.coordinates[0, 1],
            color="red",
        )

        self.current_coordinate_plot.set_offsets(self.ptychography.coordinates[0])
        self.mpl.draw()

    @Slot(list)
    def update_point(self, current_coordinate):
        # TODO: for each step update point color and add circle with laser spot diameter, save and display averaged frame
        self.current_coordinate_plot.set_offsets(current_coordinate)
        self.mpl.draw()

    def refresh_controller(self):
        if self.devices.count() == 0:
            self.device = MCS2_Controller()

            self.device.signals.error.connect(self.show_error)
            self.device.signals.locator.connect(self.show_locator)
            self.device.signals.update_data.connect(self.get_position)
            self.device.signals.default.connect(self.default)

            # set ptychography module d_handel to device's d_handle
            self.ptychography.d_handle = self.device.d_handle

            # TODO: TEMPORARY
            self.plus_0_button.setEnabled(True)
            self.plus_1_button.setEnabled(True)
            self.plus_2_button.setEnabled(True)
            self.step_size_0.setEnabled(True)
            self.plus_0_button.clicked.connect(partial(self.increase, 0))
            self.plus_1_button.clicked.connect(partial(self.increase, 1))
            self.plus_2_button.clicked.connect(partial(self.increase, 2))
            self.velocity_0.setEnabled(True)
            self.velocity_1.setEnabled(True)
            self.velocity_2.setEnabled(True)
            self.velocity_0.editingFinished.connect(partial(self.update_velocity, 0))
            self.velocity_1.editingFinished.connect(partial(self.update_velocity, 1))
            self.velocity_2.editingFinished.connect(partial(self.update_velocity, 2))

            self.device.initialize_controller()

    def increase(self, channel):
        if channel == 0:
            self.device.increase(channel, self.step_size_0.value())
        if channel == 1:
            self.device.increase(channel, self.step_size_1.value())
        if channel == 2:
            self.device.increase(channel, self.step_size_2.value())

    def decrease(self, channel):
        if channel == 0:
            self.device.decrease(channel, self.step_size_0.value())
        if channel == 1:
            self.device.decrease(channel, self.step_size_1.value())
        if channel == 2:
            self.device.decrease(channel, self.step_size_2.value())

    def refresh_camera(self):
        if self.cameras.count() == 0:
            self.camera = ScientificCamera()
            self.camera.start()

            self.directory_label.setText(str(os.getcwd()))

            self.camera.frame_signal.connect(self.setImage)
            self.camera.model_signal.connect(self.show_model)
            self.capture_button.clicked.connect(self.capture)
            self.exposure.valueChanged.connect(self.camera.update_exposure)
            self.directory_button.clicked.connect(self.select_directory)
            self.stop_button.clicked.connect(self.stop_camera)

            # set ptychography module camera to scientific camera
            self.ptychography.camera = self.camera

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
        self.plus_0_button.setEnabled(True)
        self.plus_1_button.setEnabled(True)
        self.plus_2_button.setEnabled(True)
        self.minus_0_button.setEnabled(True)
        self.minus_1_button.setEnabled(True)
        self.minus_2_button.setEnabled(True)
        self.step_size_0.setEnabled(True)
        self.step_size_1.setEnabled(True)
        self.step_size_2.setEnabled(True)

        # add movement modes
        self.move_mode_select.addItem("Absolute Mode")
        self.move_mode_select.addItem("Relative Mode")

        self.move_mode_select.currentIndexChanged.connect(self.device.set_movement_mode)

        # update position value for each channel
        self.position_0.editingFinished.connect(partial(self.update_position, 0))
        self.position_0.editingFinished.connect(partial(self.update_position, 1))
        self.position_0.editingFinished.connect(partial(self.update_position, 2))

        # update velocity for each channel
        self.velocity_0.editingFinished.connect(partial(self.update_velocity, 0))
        self.velocity_1.editingFinished.connect(partial(self.update_velocity, 1))
        self.velocity_2.editingFinished.connect(partial(self.update_velocity, 2))

        # update acceleration for each channel
        self.acceleration_0.editingFinished.connect(
            partial(self.update_acceleration, 0)
        )
        self.acceleration_1.editingFinished.connect(
            partial(self.update_acceleration, 1)
        )
        self.acceleration_2.editingFinished.connect(
            partial(self.update_acceleration, 2)
        )

        # add incremental steps for each channel
        self.plus_0_button.clicked.connect(partial(self.increase, 0))
        self.plus_1_button.clicked.connect(partial(self.increase, 1))
        self.plus_2_button.clicked.connect(partial(self.increase, 2))

        self.minus_0_button.clicked.connect(partial(self.decrease, 0))
        self.minus_1_button.clicked.connect(partial(self.decrease, 1))
        self.minus_2_button.clicked.connect(partial(self.decrease, 2))

        # add functionality to reference and calibrate buttons
        self.reference_button.clicked.connect(self.device.reference)
        self.calibrate_button.clicked.connect(self.device.calibrate)

    def update_position(self, channel):
        if channel == 0:
            print(f"{channel}, {self.position_0.value()}")
            self.device.set_position(channel, self.position_0.value())
        if channel == 1:
            print(f"{channel}, {self.position_1.value()}")
            self.device.set_position(channel, self.position_1.value())
        if channel == 2:
            print(f"{channel}, {self.position_2.value()}")
            self.device.set_position(channel, self.position_2.value())

    def update_velocity(self, channel):
        if channel == 0:
            print(f"{channel}, {self.velocity_0.value()}")
            self.device.set_velocity(channel, self.velocity_0.value())
        if channel == 1:
            print(f"{channel}, {self.velocity_1.value()}")
            self.device.set_velocity(channel, self.velocity_1.value())
        if channel == 2:
            print(f"{channel}, {self.velocity_2.value()}")
            self.device.set_velocity(channel, self.velocity_2.value())

    def update_acceleration(self, channel):
        if channel == 0:
            print(f"{channel}, {self.acceleration_0.value()}")
            self.device.set_acceleration(channel, self.acceleration_0.value())
        if channel == 1:
            print(f"{channel}, {self.acceleration_1.value()}")
            self.device.set_acceleration(channel, self.acceleration_1.value())
        if channel == 2:
            print(f"{channel}, {self.acceleration_2.value()}")
            self.device.set_acceleration(channel, self.acceleration_2.value())

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

    # TODO: add z position centering for algorithm

    def move(self):
        # add movement functionality
        # convert to pm by multiplying by 1000
        print(self.move_form.position_0.value())
        positions = [
            self.move_form.position_0.value() * 1000,
            self.move_form.position_1.value() * 1000,
            self.move_form.position_2.value() * 1000,
        ]
        self.device.move(positions)

    @Slot(list)
    def get_position(self, position):
        self.position_0.setValue(position[0])
        self.position_1.setValue(position[1])
        self.position_2.setValue(position[2])

    # safely close connection to Controller
    # TODO: decouple
    def closeEvent(self, event):
        # easier to ask for forgiveness than permission (EAFP)
        try:
            if self.device.d_handle is not None:
                # ctl.Close(self.device.d_handle)
                pass
        except AttributeError:
            pass

        super(QMainWindow, self).closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()
