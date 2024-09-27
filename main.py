import numpy as np
import pyqtgraph as pg  # type: ignore
from scipy.spatial.distance import cdist  # type: ignore

# TODO: IMPLEMENT MVP/MVVM Architecture + Observer Pattern for asynchronous model updates

# create window
win: pg.GraphicsLayoutWidget = pg.GraphicsLayoutWidget(
    show=True, title="Vogel's Spiral"
)

win.resize(600, 600)
pg.setConfigOptions(antialias=True)  # enable antialiasing

p1: pg.PlotItem = win.addPlot(title="Fermat's Spiral & Ptychographic Trajectory")


def create_fermat_spiral(
    n_points: int = 119, radius: float = 10.0, shift: bool = False
) -> np.ndarray:
    """create_fermat_spiral summary

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
    # create fermat spiral
    n_index: np.ndarray = np.arange(0, n_points - 1)
    golden_angle: np.float64 = np.pi * (3 - np.sqrt(5))
    theta: np.ndarray = golden_angle * n_index

    # by dividing n_index by n_points the graph becomes normalized,
    # then multiplying by the radius gives the desired size
    r: np.float64 = radius * np.sqrt(n_index / n_points)
    x: np.float64 = r * np.cos(theta)
    y: np.float64 = r * np.sin(theta)

    # shift image to (0, 0) => no negative coordinate points
    if shift:
        x -= np.min(x)
        y -= np.min(y)

    coordinates: np.ndarray = np.vstack((x, y), dtype=np.float64).T
    return coordinates


def order_by_distance(point: np.ndarray, coordinates: np.ndarray) -> np.ndarray:
    index: np.ndarray = cdist([point], coordinates, "sqeuclidean")

    if index.size:
        result: np.ndarray = coordinates[index.argmin()]
        return result

    return np.empty(shape=(1, 2))


# voglio fare uno scan con una certa taglia, con un passo tra r/2 & r/3 (1micron)
# misura dimensione di fascio (3 micron circa ) knife edge -> misura diametro
def create_trajectory(initial_point: np.ndarray, coordinates: np.ndarray) -> np.ndarray:
    size: int = 0
    current_coordinates: np.ndarray = coordinates
    sorted_coordinates: np.ndarray = np.array([initial_point], dtype=np.float64)

    while size < coordinates.size // 2:
        # much faster:
        mask: np.ndarray = (
            cdist(current_coordinates, sorted_coordinates, "sqeuclidean") == 0
        )
        current_coordinates = np.delete(current_coordinates, mask.any(axis=1), axis=0)

        result: np.ndarray = order_by_distance(
            sorted_coordinates[-1], current_coordinates
        )
        sorted_coordinates = np.vstack([sorted_coordinates, result], dtype=np.float64)

        size += 1

    return sorted_coordinates


# algorithm to find the shortest trajectory based on the initial point, then choose that trajectory
def shortest_trajectory(coordinates: np.ndarray) -> np.ndarray:
    distances: np.ndarray = np.array([], dtype=np.float64)

    for point in coordinates:
        diff: np.ndarray = np.diff(create_trajectory(point, coordinates), axis=0)
        total_distance: np.ndarray = np.hypot(diff[:, 0], diff[:, 1]).sum()
        distances = np.append(distances, total_distance)

    trajectory: np.ndarray = create_trajectory(
        coordinates[distances.argmin()], coordinates
    )

    return trajectory


coordinates: np.ndarray = create_fermat_spiral()

p1.plot(
    coordinates, pen=None, name="positive", symbol="o", symbolBrush="g", symbolPen="r"
)
p1.plot(
    coordinates,
    pen=None,
    name="Circles",
    symbol="o",
    symbolBrush=None,
    symbolPen="b",
    symbolSize=2,
    pxMode=False,
)

curve: pg.PlotDataItem = p1.plot(
    shortest_trajectory(coordinates), pen="r", name="positive"
)

if __name__ == "__main__":
    pg.exec()
