import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
from sfla import gen_frogs

frogs = gen_frogs(5, 2, 5, 6)

print(frogs)

fig, ax = plt.subplots()
ax.scatter(*frogs.T) 

path = frogs

# reading the image
image = plt.imread('frog.png')
# OffsetBox
image_box = OffsetImage(image, zoom=0.03)


for x0, y0 in frogs:
    ab = AnnotationBbox(image_box, (x0, y0), frameon=False)
    ax.add_artist(ab)
ax.scatter(50, 50)
ax.plot(*path.T)
plt.show()