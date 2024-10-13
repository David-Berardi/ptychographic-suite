import numpy as np
import smaract.ctl as ctl  # type: ignore
from PySide6.QtCore import QObject, QTimer, Signal, Slot


class Signals(QObject):
    error = Signal(str)
    locator = Signal(str)
    update_data = Signal(list)
    default = Signal(list)


# NOTE: when the controller boots, the initial position is set to zero whatever physical position it is in.
# therefore referencing is needed + set new zeroth position
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

        self.timer.start()

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
                self.signals.default.emit([1000000, 100000000])  # TEMPORARY
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

            default_velocity = 1000000000
            default_acceleration = 1000000000

            # default velocity for all channels [in pm/s]
            ctl.SetProperty_i64(
                self.d_handle, 0, ctl.Property.MOVE_VELOCITY, default_velocity
            )
            ctl.SetProperty_i64(
                self.d_handle, 1, ctl.Property.MOVE_VELOCITY, default_velocity
            )
            ctl.SetProperty_i64(
                self.d_handle, 2, ctl.Property.MOVE_VELOCITY, default_velocity
            )

            # default acceleration for all channels [in pm/s2]
            ctl.SetProperty_i64(
                self.d_handle, 0, ctl.Property.MOVE_ACCELERATION, default_acceleration
            )
            ctl.SetProperty_i64(
                self.d_handle, 1, ctl.Property.MOVE_ACCELERATION, default_acceleration
            )
            ctl.SetProperty_i64(
                self.d_handle, 2, ctl.Property.MOVE_ACCELERATION, default_acceleration
            )

            # TODO: update interface with default velocity and acceleration
            self.signals.default.emit([default_velocity, default_acceleration])
            print(default_velocity)

            # start data acquisition
            self.timer.start()

        except Exception as e:
            self.signals.error.emit(
                "MCS2 failed to find devices. Exit. An exception has occured"
            )
            print("MCS2 failed to find devices. Exit. An exception has occured")
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
        if mode == 0:  # ABSOLUTE mode
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
        if mode == 1:  # RELATIVE mode
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
        ctl.SetProperty_i32(
            self.d_handle,
            0,
            ctl.Property.REFERENCING_OPTIONS,
            ctl.ReferencingOption.AUTO_ZERO,
        )

        # Set velocity to 1mm/s
        ctl.SetProperty_i64(self.d_handle, 0, ctl.Property.MOVE_VELOCITY, 1_000_000_000)
        # Set acceleration to 10mm/s2.
        ctl.SetProperty_i64(
            self.d_handle, 0, ctl.Property.MOVE_ACCELERATION, 10_000_000_000
        )
        # Start referencing sequence
        ctl.Reference(self.d_handle, 0)
        position = ctl.GetProperty_i64(self.d_handle, 0, ctl.Property.POSITION)
        # self.signals.pos.emit(position)

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
        # TODO: write as command group
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

    # TODO: when dhandle is created, emit signal with handle and slot it to creation of path generator (dhandle, camera)
