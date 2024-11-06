import sys

import numpy as np
import smaract.ctl as ctl  # type: ignore
from PySide6.QtCore import QObject, QTimer, Signal, Slot

DEBUG = True


class Signals(QObject):
    error = Signal(str)
    locator = Signal(str)
    update_data = Signal(list)
    default = Signal(list)
    finished = Signal(int)  # finished movement/calibration/referencing


# NOTE: when the controller boots, the initial position is set to zero whatever physical position it is in.
# therefore referencing is needed + set new zeroth position
class MCS2_Controller:
    def __init__(self):
        self.signals = Signals()
        self.d_handle = None

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

            try:
                # Controller Handle
                self.d_handle = ctl.Open(locator)
                self.r_id = [0] * 9

                # TODO: emit d_handle for ptychography module

                base_unit = ctl.GetProperty_i32(
                    self.d_handle, 0, ctl.Property.POS_BASE_UNIT
                )

                position = ctl.GetProperty_i64(self.d_handle, 0, ctl.Property.POSITION)
                # self.signals.pos.emit(position)
                print(f"MCS2 position of channel {0}: {position}", end="")
                print("pm.") if base_unit == ctl.BaseUnit.METER else print("ndeg.")

                default_velocity = 1_000_000_000
                default_acceleration = 10_000_000_000

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
                    self.d_handle,
                    0,
                    ctl.Property.MOVE_ACCELERATION,
                    default_acceleration,
                )
                ctl.SetProperty_i64(
                    self.d_handle,
                    1,
                    ctl.Property.MOVE_ACCELERATION,
                    default_acceleration,
                )
                ctl.SetProperty_i64(
                    self.d_handle,
                    2,
                    ctl.Property.MOVE_ACCELERATION,
                    default_acceleration,
                )

                # TODO: update interface with default velocity and acceleration
                self.signals.default.emit([default_velocity, default_acceleration])
                print(default_velocity)

                # start data acquisition
                self.timer.start()
            except ctl.Error as error:
                print(
                    f"MCS2 {error.func}: {ctl.GetResultInfo(error.code)}, error: {ctl.ErrorCode(error.code).name} (0x{error.code:04X}) in line: {sys.exc_info()[-1].tb_lineno}."
                )
            except Exception as ex:
                print(
                    f"Unexpected error: {ex}, {type(ex)} in line: {sys.exc_info()[-1].tb_lineno}"
                )
                raise

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

    def waitForEvent(self):
        """Wait for events generated by the connected device"""
        # The wait for event function blocks until an event was received or the timeout elapsed.
        # In case of timeout, a "ctl.Error" exception is raised containing the "TIMEOUT" error.
        # For this example we are only interested in "CMD_GROUP_TRIGGERED" events
        # thus we drop all other events like "MOVEMENT_FINISHED" etc.
        timeout = 10000  # in ms

        while True:
            try:
                event = ctl.WaitForEvent(self.d_handle, timeout)
                # The "type" field specifies the event.
                # The "idx" field holds the device index for this event, it will always be "0", thus might be ignored here.
                # The "i32" data field gives additional information about the event.
                if event.type == ctl.EventType.CMD_GROUP_TRIGGERED:
                    # A command group has been executed.
                    # The event parameter holds:
                    # - the result code of the group (Bit 0-15)
                    # - the corresponding transmit handle of the group (Bit 31-24)
                    t_handle = ctl.EventParameter.PARAM_HANDLE(event.i32)
                    result_code = ctl.EventParameter.PARAM_RESULT(event.i32)
                    if result_code == ctl.ErrorCode.NONE:
                        print(f"MCS2 command group triggered, handle: {t_handle}")
                    else:
                        # The command group failed -> the reason may be found in the result code.
                        # To determine which command caused the error, read the individual results of the command
                        # with "WaitForWrite" / "ReadProperty_x".
                        print(
                            f"MCS2 command group failed, handle: {t_handle}, error: 0x{result_code:04X} ({ctl.GetResultInfo(result_code)})"
                        )
                    break
                else:
                    # ignore other events and wait for the next one
                    pass
            except ctl.Error as e:
                if e.code == ctl.ErrorCode.TIMEOUT:
                    print(f"MCS2 wait for event timed out after {timeout} ms")
                else:
                    print(f"MCS2 {ctl.GetResultInfo(e.code)}")
                return

    def set_position(self, channel, position):
        if channel == 0:
            ctl.SetProperty_i64(
                self.d_handle, channel, ctl.Property.POSITION * 1000, position
            )
        if channel == 1:
            ctl.SetProperty_i64(
                self.d_handle, channel, ctl.Property.POSITION * 1000, position
            )
        if channel == 2:
            ctl.SetProperty_i64(
                self.d_handle, channel, ctl.Property.POSITION * 1000, position
            )

    def set_velocity(self, channel, velocity):
        if channel == 0:
            ctl.SetProperty_i64(
                self.d_handle, channel, ctl.Property.MOVE_VELOCITY * 1000, velocity
            )
        if channel == 1:
            ctl.SetProperty_i64(
                self.d_handle, channel, ctl.Property.MOVE_VELOCITY * 1000, velocity
            )
        if channel == 2:
            ctl.SetProperty_i64(
                self.d_handle, channel, ctl.Property.MOVE_VELOCITY * 1000, velocity
            )

    def set_acceleration(self, channel, acceleration):
        if channel == 0:
            ctl.SetProperty_i64(
                self.d_handle,
                channel,
                ctl.Property.MOVE_ACCELERATION * 1000,
                acceleration,
            )
        if channel == 1:
            ctl.SetProperty_i64(
                self.d_handle,
                channel,
                ctl.Property.MOVE_ACCELERATION * 1000,
                acceleration,
            )
        if channel == 2:
            ctl.SetProperty_i64(
                self.d_handle,
                channel,
                ctl.Property.MOVE_ACCELERATION * 1000,
                acceleration,
            )

    @Slot(int)
    def set_movement_mode(self, mode):
        if mode == 0:  # ABSOLUTE mode
            # open command group
            t_handle = ctl.OpenCommandGroup(
                self.d_handle, ctl.CmdGroupTriggerMode.DIRECT
            )

            self.r_id[0] = ctl.RequestWriteProperty_i32(
                self.d_handle,
                0,
                ctl.Property.MOVE_MODE,
                ctl.MoveMode.CL_ABSOLUTE,
                tHandle=t_handle,
            )
            self.r_id[1] = ctl.RequestWriteProperty_i32(
                self.d_handle,
                1,
                ctl.Property.MOVE_MODE,
                ctl.MoveMode.CL_ABSOLUTE,
                tHandle=t_handle,
            )
            self.r_id[2] = ctl.RequestWriteProperty_i32(
                self.d_handle,
                2,
                ctl.Property.MOVE_MODE,
                ctl.MoveMode.CL_ABSOLUTE,
                tHandle=t_handle,
            )

            # close command group
            ctl.CloseCommandGroup(self.d_handle, t_handle)

            self.waitForEvent()
            for i in range(3):
                ctl.WaitForWrite(self.d_handle, self.r_id[i])

            print(
                f"Movement Mode: {ctl.GetProperty_i32(self.d_handle, 0, ctl.Property.MOVE_MODE)} ABSOLUTE"
            )

        if mode == 1:  # RELATIVE mode
            # open command group
            t_handle = ctl.OpenCommandGroup(
                self.d_handle, ctl.CmdGroupTriggerMode.DIRECT
            )

            self.r_id[0] = ctl.RequestWriteProperty_i32(
                self.d_handle,
                0,
                ctl.Property.MOVE_MODE,
                ctl.MoveMode.CL_RELATIVE,
                tHandle=t_handle,
            )
            self.r_id[1] = ctl.RequestWriteProperty_i32(
                self.d_handle,
                1,
                ctl.Property.MOVE_MODE,
                ctl.MoveMode.CL_RELATIVE,
                tHandle=t_handle,
            )
            self.r_id[2] = ctl.RequestWriteProperty_i32(
                self.d_handle,
                2,
                ctl.Property.MOVE_MODE,
                ctl.MoveMode.CL_RELATIVE,
                tHandle=t_handle,
            )

            # close command group
            ctl.CloseCommandGroup(self.d_handle, t_handle)

            self.waitForEvent()
            for i in range(3):
                ctl.WaitForWrite(self.d_handle, self.r_id[i])

            print(
                f"Movement Mode: {ctl.GetProperty_i32(self.d_handle, 0, ctl.Property.MOVE_MODE)} RELATIVE"
            )

    @Slot()
    def reference(self):
        # open command group
        t_handle = ctl.OpenCommandGroup(self.d_handle, ctl.CmdGroupTriggerMode.DIRECT)

        # set referencing option to auto-zero
        self.r_id[0] = ctl.RequestWriteProperty_i32(
            self.d_handle,
            0,
            ctl.Property.REFERENCING_OPTIONS,
            ctl.ReferencingOption.AUTO_ZERO,
            tHandle=t_handle,
        )
        self.r_id[1] = ctl.RequestWriteProperty_i32(
            self.d_handle,
            1,
            ctl.Property.REFERENCING_OPTIONS,
            ctl.ReferencingOption.AUTO_ZERO,
            tHandle=t_handle,
        )
        self.r_id[2] = ctl.RequestWriteProperty_i32(
            self.d_handle,
            2,
            ctl.Property.REFERENCING_OPTIONS,
            ctl.ReferencingOption.AUTO_ZERO,
            tHandle=t_handle,
        )

        # Set velocity to 1mm/s
        self.r_id[3] = ctl.RequestWriteProperty_i64(
            self.d_handle,
            0,
            ctl.Property.MOVE_VELOCITY,
            1_000_000_000,
            tHandle=t_handle,
        )
        self.r_id[4] = ctl.RequestWriteProperty_i64(
            self.d_handle,
            1,
            ctl.Property.MOVE_VELOCITY,
            1_000_000_000,
            tHandle=t_handle,
        )
        self.r_id[5] = ctl.RequestWriteProperty_i64(
            self.d_handle,
            2,
            ctl.Property.MOVE_VELOCITY,
            1_000_000_000,
            tHandle=t_handle,
        )

        # Set acceleration to 10mm/s2.
        self.r_id[6] = ctl.RequestWriteProperty_i64(
            self.d_handle,
            0,
            ctl.Property.MOVE_ACCELERATION,
            10_000_000_000,
            tHandle=t_handle,
        )
        self.r_id[7] = ctl.RequestWriteProperty_i64(
            self.d_handle,
            1,
            ctl.Property.MOVE_ACCELERATION,
            10_000_000_000,
            tHandle=t_handle,
        )
        self.r_id[8] = ctl.RequestWriteProperty_i64(
            self.d_handle,
            2,
            ctl.Property.MOVE_ACCELERATION,
            10_000_000_000,
            tHandle=t_handle,
        )

        # Start referencing sequence
        ctl.Reference(self.d_handle, 0, tHandle=t_handle)
        ctl.Reference(self.d_handle, 1, tHandle=t_handle)
        ctl.Reference(self.d_handle, 2, tHandle=t_handle)

        # close command group
        ctl.CloseCommandGroup(self.d_handle, t_handle)

        self.waitForEvent()
        for id in self.r_id:
            ctl.WaitForWrite(self.d_handle, id)

        # position = ctl.GetProperty_i64(self.d_handle, 0, ctl.Property.POSITION)
        # self.signals.pos.emit(position)

        # TODO: set position to zero after referencing
        # open command group
        """ t_handle = ctl.OpenCommandGroup(self.d_handle, ctl.CmdGroupTriggerMode.DIRECT)

        self.r_id[0] = ctl.RequestWriteProperty_i64(
            self.d_handle, 0, ctl.Property.POSITION, 0, tHandle=t_handle
        )
        self.r_id[1] = ctl.RequestWriteProperty_i64(
            self.d_handle, 1, ctl.Property.POSITION, 0, tHandle=t_handle
        )
        self.r_id[2] = ctl.RequestWriteProperty_i64(
            self.d_handle, 2, ctl.Property.POSITION, 0, tHandle=t_handle
        )

        # close command group
        ctl.CloseCommandGroup(self.d_handle, t_handle)

        # optional: block and wait for event
        self.waitForEvent()
        for i in range(3):
            ctl.WaitForWrite(self.d_handle, self.r_id[i]) """

    @Slot()
    def calibrate(self):
        # open command group
        t_handle = ctl.OpenCommandGroup(self.d_handle, ctl.CmdGroupTriggerMode.DIRECT)

        # set calibration option for each channel
        self.r_id[0] = ctl.RequestWriteProperty_i32(
            self.d_handle,
            0,
            ctl.Property.CALIBRATION_OPTIONS,
            ctl.CalibrationOption.DIRECTION,
            tHandle=t_handle,
        )
        self.r_id[1] = ctl.RequestWriteProperty_i32(
            self.d_handle,
            1,
            ctl.Property.CALIBRATION_OPTIONS,
            ctl.CalibrationOption.DIRECTION,
            tHandle=t_handle,
        )
        self.r_id[2] = ctl.RequestWriteProperty_i32(
            self.d_handle,
            2,
            ctl.Property.CALIBRATION_OPTIONS,
            ctl.CalibrationOption.DIRECTION,
            tHandle=t_handle,
        )

        # Start calibration sequence
        ctl.Calibrate(self.d_handle, 0, tHandle=t_handle)
        ctl.Calibrate(self.d_handle, 1, tHandle=t_handle)
        ctl.Calibrate(self.d_handle, 2, tHandle=t_handle)

        # close command group
        ctl.CloseCommandGroup(self.d_handle, t_handle)

        # optional: block and wait for event
        self.waitForEvent()
        for i in range(3):
            ctl.WaitForWrite(self.d_handle, self.r_id[i])

        """ # TODO: write as command group
        position_x = ctl.GetProperty_i64(self.d_handle, 0, ctl.Property.POSITION)
        position_y = ctl.GetProperty_i64(self.d_handle, 1, ctl.Property.POSITION)
        position_z = ctl.GetProperty_i64(self.d_handle, 2, ctl.Property.POSITION)

        position = [position_x, position_y, position_z]

        self.signals.update_data.emit(position) """

    def move(self, positions):
        # open command group
        t_handle = ctl.OpenCommandGroup(self.d_handle, ctl.CmdGroupTriggerMode.DIRECT)

        ctl.Move(self.d_handle, 0, positions[0], tHandle=t_handle)
        ctl.Move(self.d_handle, 1, positions[1], tHandle=t_handle)
        ctl.Move(self.d_handle, 2, positions[2], tHandle=t_handle)

        # close command group
        ctl.CloseCommandGroup(self.d_handle, t_handle)

        # optional: block and wait for event
        self.waitForEvent()

        print(f"MCS2 move channel 0 to absolute position: {positions[0]} pm.")

    def increase(self, channel, increment):
        if channel == 0:
            print(f"channel: {channel}, increment: {increment}")
            ctl.Move(self.d_handle, channel, increment * 1000)
        if channel == 1:
            print(f"channel: {channel}, increment: {increment}")
            ctl.Move(self.d_handle, channel, increment * 1000)
        if channel == 2:
            print(f"channel: {channel}, increment: {increment}")
            ctl.Move(self.d_handle, channel, increment * 1000)

    def decrease(self, channel, increment):
        if channel == 0:
            print(f"channel: {channel}, increment: {increment}")
            ctl.Move(self.d_handle, channel, -increment * 1000)
        if channel == 1:
            print(f"channel: {channel}, increment: {increment}")
            ctl.Move(self.d_handle, channel, -increment * 1000)
        if channel == 2:
            print(f"channel: {channel}, increment: {increment}")
            ctl.Move(self.d_handle, channel, -increment * 1000)

    def abort(self):
        # close all channels at the same time
        # open command group
        t_handle = ctl.OpenCommandGroup(self.d_handle, ctl.CmdGroupTriggerMode.DIRECT)

        ctl.Stop(self.d_handle, 0, tHandle=t_handle)
        ctl.Stop(self.d_handle, 1, tHandle=t_handle)
        ctl.Stop(self.d_handle, 2, tHandle=t_handle)

        # close command group
        ctl.CloseCommandGroup(self.d_handle, t_handle)

        # optional: block and wait for event
        self.waitForEvent()

        print("MCS2 stop channels.")

    def update_data(self):
        """# open command group
        t_handle = ctl.OpenCommandGroup(self.d_handle, ctl.CmdGroupTriggerMode.DIRECT)

        self.r_id[0] = ctl.RequestReadProperty(
            self.d_handle, 0, ctl.Property.POSITION, tHandle=t_handle
        )
        self.r_id[1] = ctl.RequestReadProperty(
            self.d_handle, 1, ctl.Property.POSITION, tHandle=t_handle
        )
        self.r_id[2] = ctl.RequestReadProperty(
            self.d_handle, 2, ctl.Property.POSITION, tHandle=t_handle
        )

        ctl.CloseCommandGroup(self.d_handle, t_handle)

        # Wait for the "triggered" event before reading the results
        self.waitForEvent()

        position_x = ctl.ReadProperty_i64(self.d_handle, self.r_id[0])
        position_y = ctl.ReadProperty_i64(self.d_handle, self.r_id[1])
        position_z = ctl.ReadProperty_i64(self.d_handle, self.r_id[2])"""

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
