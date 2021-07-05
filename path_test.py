import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
w = 4
h = 3
d = 70
plt.figure(figsize=(w, h), dpi=d)
fig, ax = plt.subplots()
ax.axis([-3, 3, -7, -1])
string_path_data = [
    (mpath.Path.MOVETO, (0, -3)),
    (mpath.Path.CURVE4, (1, -4)),
    (mpath.Path.CURVE4, (-1, -5)),
    (mpath.Path.CURVE4, (0, -6))]

codes, verts = zip(*string_path_data)
string_path = mpath.Path(verts, codes)
patch = mpatches.PathPatch(string_path, facecolor="none", lw=2)

ax.add_patch(patch)
plt.savefig("out.png")