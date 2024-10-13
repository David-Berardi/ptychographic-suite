import numpy as np
import smaract.ctl as ctl  # type: ignore
from PySide6.QtCore import QThread, Signal, Slot
from scipy.spatial.distance import cdist  # type: ignore


# TODO: create path generator class, for paths creation to feed to the controller
class Ptychography(QThread):
    def __init__(self, d_handle, camera):
        self.d_handle = d_handle
        self.camera = camera

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

    """# Enable the amplifier.
    ctl.SetProperty_i32(d_handle, channel, ctl.Property.AMPLIFIER_ENABLED, ctl.TRUE)
    # The hold time specifies how long the position is actively held after reaching the target.
    # This property is also not persistent and set to zero by default.
    # A value of 0 deactivates the hold time feature, the constant ctl.HOLD_TIME_INFINITE sets the time to infinite.
    # (Until manually stopped by "Stop") Here we set the hold time to 1000 ms.
    ctl.SetProperty_i32(d_handle, channel, ctl.Property.HOLD_TIME, 1000)
    TODO: once found, hold indefinitely the z channel
    for each movement hold position until image save is completed
    """

    # TODO: move -> take N pictures & average -> repeat until path is finished
    # after requesting image save, in a while loop qthread sleep for 0.1 secs or less until signal written is true
    # then set done to true, remember to release the holding position of the stages
    # use ctl.WaitForEvent, check for event.type == ctl.EventType.MOVEMENT_FINISHED
    # start image acquisition in the if statement
    def acquisition(self):
        pass

    # TODO: create ptychographic path and plot coordinate points
    # for each step update point color and add circle with laser spot diameter, save and display averaged frame

    # TODO: merge saved photos with given overlap and apply Phase Retrieval Algorithm
