import numpy as np
import smaract.ctl as ctl  # type: ignore
from PySide6.QtCore import QThread, Signal, Slot
from scipy.spatial.distance import cdist  # type: ignore

CHANNEL_X = 1
CHANNEL_Y = 2
CHANNEL_Z = 0


# TODO: create path generator class, for paths creation to feed to the controller
class Ptychography(QThread):
    current_coordinate_signal = Signal(list)

    def __init__(self, d_handle=None, camera=None):
        super().__init__()

        self.d_handle = d_handle
        self.camera = camera
        self.coordinates = None
        self.directory = None
        self.frames = None
        self.center_z = 0  # nm
        self.written = False

    def fermat_spiral(
        self,
        n_points: int = 119,
        radius: float = 10.0,
        center_x: float = 0.0,
        center_y: float = 0.0,
        shift: bool = False,
    ) -> np.ndarray:
        """fermat_spiral summary

        Parameters
        ----------
        n_points : int, optional
            Number of points in the Vogel's spiral, by default 119
        radius : float, optional
            Radius of the spiral and scaling factor of distance between points, by default 10.0
        shift : bool, optional
            Translate all points to the first quadrant, by default False

        Returns
        -------
        np.ndarray
            Array of the cartesian coordinates of the points in the Vogel's spiral
        """
        # initialize fermat spiral's polar parameters
        # by dividing n_index by n_points the graph becomes normalized,
        # then multiplying by the radius gives the desired size
        n_index: np.ndarray = np.arange(0, n_points - 1)
        r: np.float64 = radius * np.sqrt(n_index / n_points)
        golden_angle: np.float64 = np.pi * (3 - np.sqrt(5))
        theta: np.ndarray = golden_angle * n_index

        # convert to cartesian coordinates
        x: np.float64 = r * np.cos(theta) + center_x
        y: np.float64 = r * np.sin(theta) + center_y

        # shift image to (0, 0) => no negative coordinate points
        if shift:
            x -= np.min(x)
            y -= np.min(y)

        coordinates: np.ndarray = np.column_stack((x, y))

        return coordinates

    def order_by_distance(
        self, point: np.ndarray, coordinates: np.ndarray
    ) -> np.ndarray:
        index: np.ndarray = cdist([point], coordinates, "sqeuclidean")

        if index.size > 0:
            result: np.ndarray = coordinates[index.argmin()]
            return result

        return np.empty(shape=(1, 2))

    # voglio fare uno scan con una certa taglia, con un passo tra r/2 & r/3 (1micron)
    # misura dimensione di fascio (3 micron circa ) knife edge -> misura diametro
    def create_trajectory(
        self, initial_point: np.ndarray, coordinates: np.ndarray
    ) -> np.ndarray:
        size: int = 0
        current_coordinates: np.ndarray = coordinates
        sorted_coordinates: np.ndarray = np.array([initial_point], dtype=np.float64)

        while size < coordinates.size // 2:
            # much faster:
            mask: np.ndarray = (
                cdist(current_coordinates, sorted_coordinates, "sqeuclidean") == 0
            )
            current_coordinates = np.delete(
                current_coordinates, mask.any(axis=1), axis=0
            )

            result: np.ndarray = self.order_by_distance(
                sorted_coordinates[-1], current_coordinates
            )
            sorted_coordinates = np.vstack(
                [sorted_coordinates, result], dtype=np.float64
            )

            size += 1

        return sorted_coordinates

    # algorithm to find the shortest trajectory based on the initial point, then choose that trajectory
    def shortest_trajectory(self, coordinates: np.ndarray) -> np.ndarray:
        distances: np.ndarray = np.array([], dtype=np.float64)

        for point in coordinates:
            diff: np.ndarray = np.diff(
                self.create_trajectory(point, coordinates), axis=0
            )
            total_distance: np.ndarray = np.hypot(diff[:, 0], diff[:, 1]).sum()
            distances = np.append(distances, total_distance)

        trajectory: np.ndarray = self.create_trajectory(
            coordinates[distances.argmin()], coordinates
        )

        return trajectory

    def generate(self, x, y, radius):
        self.coordinates = self.fermat_spiral(radius=radius, center_x=x, center_y=y)

    @Slot(bool)
    def is_written(self, written):
        # print(f"written: {written}")
        self.written = written

    # after requesting image save, in a while loop qthread sleep for 0.1 secs or less until signal written is true
    # then set done to true, remember to release the holding position of the stages
    # use ctl.WaitForEvent, check for event.type == ctl.EventType.MOVEMENT_FINISHED

    def waitForEvent(self):
        timeout = 100000  # in ms

        while True:
            try:
                event = ctl.WaitForEvent(self.d_handle, timeout)

                if event.type == ctl.EventType.MOVEMENT_FINISHED:
                    t_handle = ctl.EventParameter.PARAM_HANDLE(event.i32)
                    result_code = ctl.EventParameter.PARAM_RESULT(event.i32)
                    if result_code == ctl.ErrorCode.NONE:
                        print(f"MCS2 movement finished, handle: {t_handle}")
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

    def run(self):
        try:
            # check if d_handle and camera exist
            # TODO: make sure d_handle is assigned once connected
            if self.d_handle is not None and self.camera is not None:
                self.camera.written_signal.connect(self.is_written)

                # start acquisition sequence
                self.acquisition()

                # end of acquisition sequence
                print("Successfully terminated acquisition sequence")
            else:
                raise Exception(
                    "Failed to start procedure: either handle or camera not initialized"
                )
        except Exception as error:
            print(error)

    @Slot()
    def abort(self):
        # stop motion and terminate thread
        t_handle = ctl.OpenCommandGroup(self.d_handle, ctl.CmdGroupTriggerMode.DIRECT)

        ctl.Stop(self.d_handle, CHANNEL_X, tHandle=t_handle)
        ctl.Stop(self.d_handle, CHANNEL_Y, tHandle=t_handle)
        ctl.Stop(self.d_handle, CHANNEL_Z, tHandle=t_handle)

        # close command group
        ctl.CloseCommandGroup(self.d_handle, t_handle)

        self.terminate()

    def acquisition(self):
        r_id = [0] * 4
        self.written = False

        if self.coordinates is not None:
            # enable amplifier for each channel
            t_handle = ctl.OpenCommandGroup(
                self.d_handle, ctl.CmdGroupTriggerMode.DIRECT
            )

            r_id[0] = ctl.RequestWriteProperty_i32(
                self.d_handle,
                CHANNEL_X,
                ctl.Property.AMPLIFIER_ENABLED,
                ctl.TRUE,
                tHandle=t_handle,
            )
            r_id[1] = ctl.RequestWriteProperty_i32(
                self.d_handle,
                CHANNEL_Y,
                ctl.Property.AMPLIFIER_ENABLED,
                ctl.TRUE,
                tHandle=t_handle,
            )
            r_id[2] = ctl.RequestWriteProperty_i32(
                self.d_handle,
                CHANNEL_Z,
                ctl.Property.AMPLIFIER_ENABLED,
                ctl.TRUE,
                tHandle=t_handle,
            )

            # move z-stage to z-coordinate and hold position indefinitely (use ctl.Stop do release)
            ctl.Move(self.d_handle, 2, int(self.center_z * 1e6), tHandle=t_handle)
            r_id[3] = ctl.RequestWriteProperty_i32(
                self.d_handle,
                CHANNEL_Z,
                ctl.Property.HOLD_TIME,
                ctl.HOLD_TIME_INFINITE,
                tHandle=t_handle,
            )

            # close command group
            ctl.CloseCommandGroup(self.d_handle, t_handle)

            # optional
            for id in r_id:
                ctl.WaitForWrite(self.d_handle, id)

            # wait for MOVEMENT_FINISHED
            self.waitForEvent()

            # move to coordinate, capture image, emit current coordinate
            for coordinate in self.coordinates:
                self.current_coordinate_signal.emit(coordinate)

                # move to coordinate and hold position (commandgroup)
                t_handle = ctl.OpenCommandGroup(
                    self.d_handle, ctl.CmdGroupTriggerMode.DIRECT
                )

                # move to coordinate
                ctl.Move(
                    self.d_handle, CHANNEL_X, int(coordinate[0] * 1e6), tHandle=t_handle
                )
                ctl.Move(
                    self.d_handle, CHANNEL_Y, int(coordinate[1] * 1e6), tHandle=t_handle
                )

                # hold position
                r_id[0] = ctl.RequestWriteProperty_i32(
                    self.d_handle,
                    CHANNEL_X,
                    ctl.Property.HOLD_TIME,
                    ctl.HOLD_TIME_INFINITE,
                    tHandle=t_handle,
                )
                r_id[1] = ctl.RequestWriteProperty_i32(
                    self.d_handle,
                    CHANNEL_Y,
                    ctl.Property.HOLD_TIME,
                    ctl.HOLD_TIME_INFINITE,
                    tHandle=t_handle,
                )

                ctl.CloseCommandGroup(self.d_handle, t_handle)

                ctl.WaitForWrite(self.d_handle, r_id[0])
                ctl.WaitForWrite(self.d_handle, r_id[1])

                # before acquiring image, check for MOVEMENT_FINISHED
                self.waitForEvent()

                """ # NOTE: might need to check whether movement_finished is true while it's still holding
                # acquire images
                self.camera.capture(self.directory, self.frames)

                # wait until it's finished writing to file
                while not self.written:
                    print("not written")
                    QThread.usleep(100)
                print("written") """
                # QThread.msleep(1)

                # release holding position for x-y stages
                t_handle = ctl.OpenCommandGroup(
                    self.d_handle, ctl.CmdGroupTriggerMode.DIRECT
                )

                ctl.Stop(self.d_handle, CHANNEL_X, tHandle=t_handle)
                ctl.Stop(self.d_handle, CHANNEL_Y, tHandle=t_handle)

                ctl.CloseCommandGroup(self.d_handle, t_handle)

                self.written = False

            # stop holding z-stage, disable amplifiers
            t_handle = ctl.OpenCommandGroup(
                self.d_handle, ctl.CmdGroupTriggerMode.DIRECT
            )

            ctl.Stop(self.d_handle, CHANNEL_Z, tHandle=t_handle)

            # NOTE: do not disable amplifier

            ctl.CloseCommandGroup(self.d_handle, t_handle)

        else:
            raise Exception("No coordinates present, generate them first")

    # TODO: merge saved photos with given overlap and apply Phase Retrieval Algorithm
