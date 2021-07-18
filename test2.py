import sfla
import numpy as np
import matplotlib.pyplot as plt

obstacles = np.array([[4, 5], [6, 6], [8, 9]])
path_solver = sfla.sflaSolver(30, 5, 7, 12, 1)
cur_pos = np.array([2,3])
target = np.array([15,15])
path = np.empty((0,2))
while  np.linalg.norm(target - cur_pos) > 0.4:
    path = np.vstack((path, cur_pos))
    cur_pos, frogs, memeplexes = path_solver.sfla(cur_pos, target, obstacles)


fig, ax = plt.subplots()
ax.scatter(2,3)
ax.scatter(*obstacles.T)
ax.scatter(target[0], target[1])
ax.plot(*path.T)
plt.show()
