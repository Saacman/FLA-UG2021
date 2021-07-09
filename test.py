import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
from sfla import gen_frogs, sort_frogs, opt_func


frogs = gen_frogs(60, 10, (2,3))
print(frogs)
obstacles = np.array([[4,5]])#, [6,6], [8,9]])
#print(frogs)

fig, ax = plt.subplots()
ax.scatter(*frogs.T)
memes = sort_frogs(frogs, 6, obstacles, 5, 12, (50,50))

# reading the image
image = plt.imread('frog.png')
# OffsetBox
image_box = OffsetImage(image, zoom=0.03)


for x0, y0 in frogs:
    ab = AnnotationBbox(image_box, (x0, y0), frameon=False)
    ax.add_artist(ab)
ax.scatter(2,3)
ax.scatter(50,50) #target
#ax.plot(*path.T)
plt.show()