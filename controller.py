import sys

import numpy as np
import smaract.ctl as ctl  # type: ignore
from PySide6.QtCore import QObject, QTimer, Signal, Slot

CHANNEL_X = 1
CHANNEL_Y = 2
CHANNEL_Z = 0


class Signals(QObject):
    error = Signal(str)
    locator = Signal(str)
    update_data = Signal(list)
    default = Signal(list)
    finished = Signal(int)  # finished movement/calibration/referencing


# NOTE: when the controller boots, the initial position is set to zero whatever physical position it is in.
# therefore referencing is needed + set new zeroth position

# NOTE: no need for qthread due to connection to controller already async (and commands -> they're sent sync but processed async)

# NOTE: COMMAND_GROUPs work really well! use as much as possible to ensure best reactivity

# NOTE: to guarantee precise movement position first select movement mode (in this case RELATIVE_MODE)

# TODO: convert from nanometer to micrometer as per Prof's request -> use DoubleSpinBox


class MCS2_Controller:
    def __init__(self):
        self.signals = Signals()
        self.d_handle = None

    def initialize_controller(self):
        # setup timer for data polling
        self.timer = QTimer()
        self.timer.setInterval(750)  # ms
        self.timer.timeout.connect(self.update_data)

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
            # locator = "network:192.168.7.8"

            if len(buffer) == 0:
                self.signals.error.emit("MCS2 no devices found.")
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

                base_unit = ctl.GetProperty_i32(
                    self.d_handle, CHANNEL_X, ctl.Property.POS_BASE_UNIT
                )

                position = ctl.GetProperty_i64(
                    self.d_handle, CHANNEL_Z, ctl.Property.POSITION
                )
                print(f"MCS2 position of channel {CHANNEL_Z}: {position}", end="")
                print("pm.") if base_unit == ctl.BaseUnit.METER else print("ndeg.")

                # start timer
                self.timer.start()

                default_velocity = 1_000_000_000
                default_acceleration = 10_000_000_000

                t_handle = ctl.OpenCommandGroup(
                    self.d_handle, ctl.CmdGroupTriggerMode.DIRECT
                )

                # default velocity for all channels [in pm/s]
                ctl.RequestWriteProperty_i64(
                    self.d_handle,
                    CHANNEL_X,
                    ctl.Property.MOVE_VELOCITY,
                    default_velocity,
                    tHandle=t_handle,
                )
                ctl.RequestWriteProperty_i64(
                    self.d_handle,
                    CHANNEL_Y,
                    ctl.Property.MOVE_VELOCITY,
                    default_velocity,
                    tHandle=t_handle,
                )
                ctl.RequestWriteProperty_i64(
                    self.d_handle,
                    CHANNEL_Z,
                    ctl.Property.MOVE_VELOCITY,
                    default_velocity,
                    tHandle=t_handle,
                )

                # default acceleration for all channels [in pm/s2]
                ctl.RequestWriteProperty_i64(
                    self.d_handle,
                    CHANNEL_X,
                    ctl.Property.MOVE_ACCELERATION,
                    default_acceleration,
                    tHandle=t_handle,
                )
                ctl.RequestWriteProperty_i64(
                    self.d_handle,
                    CHANNEL_Y,
                    ctl.Property.MOVE_ACCELERATION,
                    default_acceleration,
                    tHandle=t_handle,
                )
                ctl.RequestWriteProperty_i64(
                    self.d_handle,
                    CHANNEL_Z,
                    ctl.Property.MOVE_ACCELERATION,
                    default_acceleration,
                    tHandle=t_handle,
                )

                ctl.CloseCommandGroup(self.d_handle, t_handle)

                # update interface with default velocity and acceleration
                self.signals.default.emit(
                    [default_velocity / 1e6, default_acceleration / 1e6]
                )

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

    # position is in micrometers -> convert to picometers
    def set_position(self, channel, position):
        if channel == CHANNEL_X:
            ctl.SetProperty_i64(
                self.d_handle, channel, ctl.Property.POSITION, int(position * 1e6)
            )
        if channel == CHANNEL_Y:
            ctl.SetProperty_i64(
                self.d_handle, channel, ctl.Property.POSITION, int(position * 1e6)
            )
        if channel == CHANNEL_Z:
            ctl.SetProperty_i64(
                self.d_handle, channel, ctl.Property.POSITION, int(position * 1e6)
            )

    def set_velocity(self, channel, velocity):
        if channel == CHANNEL_X:
            ctl.SetProperty_i64(
                self.d_handle, channel, ctl.Property.MOVE_VELOCITY, int(velocity * 1e6)
            )
        if channel == CHANNEL_Y:
            ctl.SetProperty_i64(
                self.d_handle, channel, ctl.Property.MOVE_VELOCITY, int(velocity * 1e6)
            )
        if channel == CHANNEL_Z:
            ctl.SetProperty_i64(
                self.d_handle, channel, ctl.Property.MOVE_VELOCITY, int(velocity * 1e6)
            )

    def set_acceleration(self, channel, acceleration):
        if channel == CHANNEL_X:
            ctl.SetProperty_i64(
                self.d_handle,
                channel,
                ctl.Property.MOVE_ACCELERATION,
                int(acceleration * 1e6),
            )
        if channel == CHANNEL_Y:
            ctl.SetProperty_i64(
                self.d_handle,
                channel,
                ctl.Property.MOVE_ACCELERATION,
                int(acceleration * 1e6),
            )
        if channel == CHANNEL_Z:
            ctl.SetProperty_i64(
                self.d_handle,
                channel,
                ctl.Property.MOVE_ACCELERATION,
                int(acceleration * 1e6),
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
                CHANNEL_X,
                ctl.Property.MOVE_MODE,
                ctl.MoveMode.CL_ABSOLUTE,
                tHandle=t_handle,
            )
            self.r_id[1] = ctl.RequestWriteProperty_i32(
                self.d_handle,
                CHANNEL_Y,
                ctl.Property.MOVE_MODE,
                ctl.MoveMode.CL_ABSOLUTE,
                tHandle=t_handle,
            )
            self.r_id[2] = ctl.RequestWriteProperty_i32(
                self.d_handle,
                CHANNEL_Z,
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
                f"Movement Mode: {ctl.GetProperty_i32(self.d_handle, CHANNEL_X, ctl.Property.MOVE_MODE)} ABSOLUTE"
            )

        if mode == 1:  # RELATIVE mode
            # open command group
            t_handle = ctl.OpenCommandGroup(
                self.d_handle, ctl.CmdGroupTriggerMode.DIRECT
            )

            self.r_id[0] = ctl.RequestWriteProperty_i32(
                self.d_handle,
                CHANNEL_X,
                ctl.Property.MOVE_MODE,
                ctl.MoveMode.CL_RELATIVE,
                tHandle=t_handle,
            )
            self.r_id[1] = ctl.RequestWriteProperty_i32(
                self.d_handle,
                CHANNEL_Y,
                ctl.Property.MOVE_MODE,
                ctl.MoveMode.CL_RELATIVE,
                tHandle=t_handle,
            )
            self.r_id[2] = ctl.RequestWriteProperty_i32(
                self.d_handle,
                CHANNEL_Z,
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
                f"Movement Mode: {ctl.GetProperty_i32(self.d_handle, CHANNEL_X, ctl.Property.MOVE_MODE)} RELATIVE"
            )

    @Slot()
    def reference(self):
        # open command group
        t_handle = ctl.OpenCommandGroup(self.d_handle, ctl.CmdGroupTriggerMode.DIRECT)

        # set referencing option to auto-zero
        self.r_id[0] = ctl.RequestWriteProperty_i32(
            self.d_handle,
            CHANNEL_X,
            ctl.Property.REFERENCING_OPTIONS,
            ctl.ReferencingOption.AUTO_ZERO,
            tHandle=t_handle,
        )
        self.r_id[1] = ctl.RequestWriteProperty_i32(
            self.d_handle,
            CHANNEL_Y,
            ctl.Property.REFERENCING_OPTIONS,
            ctl.ReferencingOption.AUTO_ZERO,
            tHandle=t_handle,
        )
        self.r_id[2] = ctl.RequestWriteProperty_i32(
            self.d_handle,
            CHANNEL_Z,
            ctl.Property.REFERENCING_OPTIONS,
            ctl.ReferencingOption.AUTO_ZERO,
            tHandle=t_handle,
        )

        """ # Set velocity to 1mm/s
        self.r_id[3] = ctl.RequestWriteProperty_i64(
            self.d_handle,
            CHANNEL_X,
            ctl.Property.MOVE_VELOCITY,
            10_000_000_000,
            tHandle=t_handle,
        )
        self.r_id[4] = ctl.RequestWriteProperty_i64(
            self.d_handle,
            CHANNEL_Y,
            ctl.Property.MOVE_VELOCITY,
            10_000_000_000,
            tHandle=t_handle,
        )
        self.r_id[5] = ctl.RequestWriteProperty_i64(
            self.d_handle,
            CHANNEL_Z,
            ctl.Property.MOVE_VELOCITY,
            10_000_000_000,
            tHandle=t_handle,
        )

        # Set acceleration to 10mm/s2.
        self.r_id[6] = ctl.RequestWriteProperty_i64(
            self.d_handle,
            CHANNEL_X,
            ctl.Property.MOVE_ACCELERATION,
            100_000_000_000,
            tHandle=t_handle,
        )
        self.r_id[7] = ctl.RequestWriteProperty_i64(
            self.d_handle,
            CHANNEL_Y,
            ctl.Property.MOVE_ACCELERATION,
            10_000_000_000,
            tHandle=t_handle,
        )
        self.r_id[8] = ctl.RequestWriteProperty_i64(
            self.d_handle,
            CHANNEL_Z,
            ctl.Property.MOVE_ACCELERATION,
            10_000_000_000,
            tHandle=t_handle,
        ) """

        # Start referencing sequence
        ctl.Reference(self.d_handle, CHANNEL_X, tHandle=t_handle)
        ctl.Reference(self.d_handle, CHANNEL_Y, tHandle=t_handle)
        ctl.Reference(self.d_handle, CHANNEL_Z, tHandle=t_handle)

        # close command group
        ctl.CloseCommandGroup(self.d_handle, t_handle)

        self.waitForEvent()
        for id in self.r_id:
            ctl.WaitForWrite(self.d_handle, id)

        # with AUTO_ZERO no need to set position to zero after referencing

    @Slot()
    def calibrate(self):
        # open command group
        t_handle = ctl.OpenCommandGroup(self.d_handle, ctl.CmdGroupTriggerMode.DIRECT)

        # set calibration option for each channel
        self.r_id[0] = ctl.RequestWriteProperty_i32(
            self.d_handle,
            CHANNEL_X,
            ctl.Property.CALIBRATION_OPTIONS,
            ctl.CalibrationOption.DIRECTION,
            tHandle=t_handle,
        )
        self.r_id[1] = ctl.RequestWriteProperty_i32(
            self.d_handle,
            CHANNEL_Y,
            ctl.Property.CALIBRATION_OPTIONS,
            ctl.CalibrationOption.DIRECTION,
            tHandle=t_handle,
        )
        self.r_id[2] = ctl.RequestWriteProperty_i32(
            self.d_handle,
            CHANNEL_Z,
            ctl.Property.CALIBRATION_OPTIONS,
            ctl.CalibrationOption.DIRECTION,
            tHandle=t_handle,
        )

        # Start calibration sequence
        ctl.Calibrate(self.d_handle, CHANNEL_X, tHandle=t_handle)
        ctl.Calibrate(self.d_handle, CHANNEL_Y, tHandle=t_handle)
        ctl.Calibrate(self.d_handle, CHANNEL_Z, tHandle=t_handle)

        # close command group
        ctl.CloseCommandGroup(self.d_handle, t_handle)

        # optional: block and wait for event
        self.waitForEvent()
        for i in range(3):
            ctl.WaitForWrite(self.d_handle, self.r_id[i])

        """ # TODO: write as command group
        position_x = ctl.GetProperty_i64(self.d_handle, CHANNEL_X, ctl.Property.POSITION)
        position_y = ctl.GetProperty_i64(self.d_handle, CHANNEL_Y, ctl.Property.POSITION)
        position_z = ctl.GetProperty_i64(self.d_handle, CHANNEL_Z, ctl.Property.POSITION)

        position = [position_x, position_y, position_z]

        self.signals.update_data.emit(position) """

    # TODO: convert from microm to pm
    def move(self, positions):
        # open command group
        t_handle = ctl.OpenCommandGroup(self.d_handle, ctl.CmdGroupTriggerMode.DIRECT)

        ctl.Move(self.d_handle, CHANNEL_X, int(positions[0] * 1e6), tHandle=t_handle)
        ctl.Move(self.d_handle, CHANNEL_Y, int(positions[1] * 1e6), tHandle=t_handle)
        ctl.Move(self.d_handle, CHANNEL_Z, int(positions[2] * 1e6), tHandle=t_handle)

        # close command group
        ctl.CloseCommandGroup(self.d_handle, t_handle)

        # optional: block and wait for event
        self.waitForEvent()

        print(f"MCS2 move channel 0 to absolute relative: {positions[0]} pm.")

    def increase(self, channel, increment):
        if channel == CHANNEL_X:
            print(f"channel: {channel}, increment: {increment* 1e6}")
            ctl.Move(self.d_handle, channel, int(increment * 1e6))
        if channel == CHANNEL_Y:
            print(f"channel: {channel}, increment: {increment* 1e6}")
            ctl.Move(self.d_handle, channel, int(increment * 1e6))
        if channel == CHANNEL_Z:
            print(f"channel: {channel}, increment: {increment* 1e6}")
            ctl.Move(self.d_handle, channel, int(increment * 1e6))

    def decrease(self, channel, increment):
        if channel == CHANNEL_X:
            print(f"channel: {channel}, increment: {increment* 1e6}")
            ctl.Move(self.d_handle, channel, int(-increment * 1e6))
        if channel == CHANNEL_Y:
            print(f"channel: {channel}, increment: {increment* 1e6}")
            ctl.Move(self.d_handle, channel, int(-increment * 1e6))
        if channel == CHANNEL_Z:
            print(f"channel: {channel}, increment: {increment* 1e6}")
            ctl.Move(self.d_handle, channel, int(-increment * 1e6))

    def abort(self):
        # close all channels at the same time
        # open command group
        t_handle = ctl.OpenCommandGroup(self.d_handle, ctl.CmdGroupTriggerMode.DIRECT)

        ctl.Stop(self.d_handle, CHANNEL_X, tHandle=t_handle)
        ctl.Stop(self.d_handle, CHANNEL_Y, tHandle=t_handle)
        ctl.Stop(self.d_handle, CHANNEL_Z, tHandle=t_handle)

        # close command group
        ctl.CloseCommandGroup(self.d_handle, t_handle)

        # optional: block and wait for event
        self.waitForEvent()

        print("MCS2 stop channels.")

    # convert from pm to microm
    def update_data(self):
        # open command group
        t_handle = ctl.OpenCommandGroup(self.d_handle, ctl.CmdGroupTriggerMode.DIRECT)

        self.r_id[0] = ctl.RequestReadProperty(
            self.d_handle, CHANNEL_X, ctl.Property.POSITION, tHandle=t_handle
        )
        self.r_id[1] = ctl.RequestReadProperty(
            self.d_handle, CHANNEL_Y, ctl.Property.POSITION, tHandle=t_handle
        )
        self.r_id[2] = ctl.RequestReadProperty(
            self.d_handle, CHANNEL_Z, ctl.Property.POSITION, tHandle=t_handle
        )

        ctl.CloseCommandGroup(self.d_handle, t_handle)

        # DO NOT Wait for the "triggered" event before reading the results -> slows down GUI
        # self.waitForEvent()

        # TODO: remember to send float to 2 decimals
        position_x = ctl.ReadProperty_i64(self.d_handle, self.r_id[0]) / 1e6
        position_y = ctl.ReadProperty_i64(self.d_handle, self.r_id[1]) / 1e6
        position_z = ctl.ReadProperty_i64(self.d_handle, self.r_id[2]) / 1e6

        position = [position_x, position_y, position_z]

        self.signals.update_data.emit(position)
