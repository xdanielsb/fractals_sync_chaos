"""
    Copyright (C) 2021  github.com/xdanielsb
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
"""
import numpy as np
import random
from matplotlib import pyplot as plt
import matplotlib.patches as patches


def carpet(p, q, s0, it):
    def get_square(x, y, sx, sy, fill="none"):
        rect = patches.Rectangle(
            (x, y), sx, sy, linewidth=1, edgecolor="black", facecolor=fill
        )
        return rect

    def get_mid(n):
        # q is small then bruteforce
        a, b = 0, 100
        for i in range(1, n):
            if i * (n//i) == n and abs(i - n//i) < abs(a-b):
                a, b = i, n // i
        return a, b

    def div(rect, a, b, remove_randomly=False):
        rects = []
        x0, y0, x1, y1 = rect
        lenx = (x1 - x0)/a
        leny = (y1 - y0)/b
        for j in range(b):
            x0 = rect[0]
            for k in range(a):
                rects.append([x0, y0, x0+lenx, y0+leny])
                x0 += lenx
            y0 += leny

        for j in range(p):
            if remove_randomly:
                rects.remove(random.choice(rects))
            else:
                rects.pop((q // 2) % len(rects))
        return rects

    a, b = get_mid(q)
    gens = [s0]
    fig, ax = plt.subplots()
    for i in range(it):
        cur = []
        for c in gens[-1]:
            cur.extend(div(c, a, b))
        gens.append(np.array(cur))

    plt.scatter([s0[-1]], [s0[-1]])
    for i, g in enumerate(gens):
        c = np.random.rand(3,)
        for x0, y0, x1, y1 in g:
            ax.add_patch(get_square(x0, y0, x1-x0, y1-y0, fill=c))

    plt.show()


if __name__ == "__main__":
    # first square bottom left, top right coordinates
    cod = 9
    s0 = [0, 0, cod*10, cod*10]
    carpet(1, cod, [s0], 3)
