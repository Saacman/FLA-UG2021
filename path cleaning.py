import matplotlib.pyplot as plt
import numpy as np
from mapping import transformB2A, GridMap
import sfla


# img = "map.png"
# mp = GridMap.loadImg(img)
# grid = mp.getGrid()
# plt.imshow(grid)
# plt.show()


grid = np.zeros((20,20))
grid[3,:14] = 1
grid[7, 6:] = 1
grid[11,:14] = 1
grid[15, 6:] = 1

result = np.where(grid == 1)

obstacles = list(zip(result[1], result[0]))
print(obstacles)
plt.imshow(grid)
plt.show()
obstacles=np.array(obstacles)

path_solver = sfla.sflaSolver(30, 5, 8, 5, 1)
cur_pos = np.array([17,17])
target = np.array([17,9])
path = np.empty((0,2))
while  np.linalg.norm(target - cur_pos) > 0.4:
    path = np.vstack((path, cur_pos))
    cur_pos, frogs, memeplexes = path_solver.sfla(cur_pos, target, obstacles)
    print("Step")

fig, ax = plt.subplots()
ax.scatter(*obstacles.T)
ax.scatter(target[1], target[0])
ax.scatter(cur_pos[1],cur_pos[0])
ax.plot(*path.T)
plt.show()
