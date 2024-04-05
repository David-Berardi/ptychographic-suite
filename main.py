import numpy as np
import pyqtgraph as pg
#from pyqtgraph.Qt import QtCore

# create app
app = pg.mkQApp("Fermat's Spiral")

# create window
win = pg.GraphicsLayoutWidget(show=True, title="Fermat's Spiral Plot")
win.resize(600, 600)
# enable antialiasing
pg.setConfigOptions(antialias=True)

p1 = win.addPlot(title="Fermat's Spiral & Ptychographic Trajectory")

def create_fermat_spiral(n_points=119, radius=10, shift=False):
    # create fermat spiral
    n_index = np.arange(0, n_points-1)
    golden_angle = np.pi*(3-np.sqrt(5))
    theta = golden_angle * n_index
    
    # compute the scaling constant such that the spiral covers an area with radius 
    #scale_constant = radius/np.sqrt(n_points)
    
    r = radius*np.sqrt(n_index/n_points) # by dividing n_index by n_points the graph becomes normalized, then multiplying by the radius gives the desired size
    x = r*np.cos(theta)
    y = r*np.sin(theta)

    # shift image to (0, 0) => no negative coordinate points
    if shift:
        x -= np.min(x)
        y -= np.min(y)
    
    #y -= np.max(y)
    
    coordinates = np.vstack((x, y), dtype=np.float64).T
    #negative = np.column_stack((-x, -y))
    #coordinates = np.vstack([coordinates, negative], dtype=np.float64)
    #coordinates[:,1] = coordinates[:,1] - np.max(coordinates[:,1])
    #print(coordinates.min())
    return coordinates


coordinates = create_fermat_spiral()
#negative = np.column_stack((-x, -y))
#coordinates = np.vstack([coordinates, negative], dtype=np.float64)

#p1.plot(x, y, pen=None, name="positive", symbol="o", symbolBrush="g", symbolPen="r")
#p1.plot(-x, -y, pen=None, name="negative", symbol="o", symbolBrush="r", symbolPen="g")
#p1.plot(x, y, pen="r", name="positive")

from scipy.spatial.distance import cdist

def order_by_distance(point, space):
    index = cdist([point], space, "sqeuclidean")
    if index.size:
        result = space[index.argmin()]
        return result
    return np.empty(shape=(1,2))

# voglio fare uno scan con una certa taglia, con un passo tra r/2 & r/3 (1micron)
# misura dimensione di fascio (3 micron circa ) knife edge -> misura diametro
def create_trajectory(initial_point):
    size = 0
    test_coordinates = coordinates
    #sorted_coordinates = np.array([coordinates[np.random.choice(coordinates.size // 2)]], dtype=np.float64)
    sorted_coordinates = np.array([initial_point], dtype=np.float64)
    
    while size < coordinates.size // 2:
        # really slow
        """
        mem = test_coordinates
        for item in sorted_coordinates:
            for index, test in enumerate(mem):
                if (item == test).all():
                    test_coordinates = np.delete(test_coordinates, index, axis=0)
        """  
             
        #much faster:
        mask = cdist(test_coordinates, sorted_coordinates, "sqeuclidean") == 0
        test_coordinates = np.delete(test_coordinates, mask.any(axis=1), axis=0)
        
        #print(f"Epoch: {size}; starting: {sorted_coordinates}, deleted: {test_coordinates[mask.any(axis=1)]}")
        #mask = cdist(test_coordinates, sorted_coordinates) == 0
        #print(f"starting: {sorted_coordinates}, deleted: {test_coordinates[mask.any(axis=1)]}")
        #print(np.delete(test_coordinates, mask))
                    
        result = order_by_distance(sorted_coordinates[-1], test_coordinates)
        sorted_coordinates = np.vstack([sorted_coordinates, result], dtype=np.float64)
        
        size += 1
    
    return sorted_coordinates

# algorithm to find the shortest trajectory based on the initial point, then choose that trajectory
def shortest_trajectory():
    distances = np.array([])
    for point in coordinates:
        diff = np.diff(create_trajectory(point), axis=0)
        total_distance = np.hypot(diff[:,0], diff[:,1]).sum()
        distances = np.append(distances, total_distance)

    trajectory = create_trajectory(coordinates[distances.argmin()])
    return trajectory


p1.plot(coordinates, pen=None, name="positive", symbol="o", symbolBrush="g", symbolPen="r")
p1.plot(coordinates, pen=None, name="Circles", symbol="o", symbolBrush=None, symbolPen="b", symbolSize=2, pxMode=False)

#data = create_trajectory()
#curve = p1.plot(create_trajectory(coordinates[0]), pen="r", name="positive")
#curve = p1.plot(shortest_trajectory(), pen="r", name="positive")

"""
# animation
def update():
    global data
    curve.setData(data)
    data = create_trajectory()
    
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10)
"""

if __name__ == '__main__':
    pg.exec()