import sfla
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


obstacles = np.array([[1, 5], [4, 2], [8, 2], [15, 1], [5, 6], [13, 6], [16, 5], 
                     [18, 3], [9, 8], [14, 8], [18, 6], [2, 10], [5, 11], [5, 12],
                      [8, 12], [14, 12], [18,12], [1,18], [4,15], [7, 17], [10, 18], [11, 15], [16, 16]])
np.save('obstacles.npy', obstacles)
path_solver = sfla.sflaSolver(30, 5, 7, 12, 1)
cur_pos = np.array([1, 2])
target = np.array([17,18])
path = np.empty((0,2))

fig, ax = plt.subplots()
ax.scatter(cur_pos[0], cur_pos[1])

while  np.linalg.norm(target - cur_pos) > 0.4:
    path = np.vstack((path, cur_pos))
    cur_pos, frogs, memeplexes = path_solver.sfla(cur_pos, target, obstacles)

ax.plot(*path.T)
ax.scatter(*obstacles.T)
ax.scatter(target[0], target[1])

ax.scatter(*path.T)
image = plt.imread('frog.png')
image_box = OffsetImage(image, zoom=0.03)
for x0, y0 in path:
    ab = AnnotationBbox(image_box, (x0, y0), frameon=False)
    ax.add_artist(ab)
    
plt.show()
