import matplotlib.pyplot as plt
import matplotlib.colors as mplc
import numpy as np

line = lambda x, b: x + b

lines = np.array(
        [line(np.linspace(0, 1, 100), b)
         for b in np.linspace(0, 1, 100)]
        )

cmap = plt.get_cmap('viridis', lines.shape[0])
norm = mplc.Normalize(vmin=0, vmax=lines.shape[0] - 1)

for i, l in enumerate(lines):
    plt.plot(l, color=cmap(norm(i)))
plt.title('color by number')
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
plt.colorbar(sm)
plt.show()
