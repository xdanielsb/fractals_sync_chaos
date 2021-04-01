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
import math


def cantor(p, q, s0, it):
    """
    s0 : length of the initial line
    it : number of iterations to print
    """

    def div(li, remove_randomly=False):
        lseq = (li[1] - li[0]) / q
        x0 = li[0]
        lines = []
        for j in range(q):
            lines.append([x0, x0 + lseq])
            x0 += lseq
        for j in range(p):
            if remove_randomly:
                lines.remove(random.choice(lines))
            else:
                lines.pop((q // 2) % len(lines))
        return lines

    lines = [np.array([s0])]
    for i in range(it):
        nlines = []
        for li in lines[-1]:
            nlines.extend(div(li))
        nlines = np.array(nlines)
        lines.append(nlines)

    for y0, nlines in enumerate(lines):
        x0, x1 = nlines[:, 0], nlines[:, 1]
        for st, end in zip(x0, x1):
            plt.plot([st, end], [y0 * 0.1, y0 * 0.1],
                     linewidth=20 / math.log(y0 + 2))
    plt.show()


if __name__ == "__main__":
    cod = 3
    s0 = [0, cod*10]  # initial state x0, x1
    cantor(1, cod, s0, 4)
