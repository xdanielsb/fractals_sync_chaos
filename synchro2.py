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

import decimal

import numpy as np
from scipy import stats

from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import cm
from random import randint

a = 10  # randint(0, 10)
b = 3  # randint(0, 10)
c = 40  # randint(0, 10)
k = 0.1


def lorentz(x1, x2, x3, h):
    global a, b, c, d, k
    x1_ = a * (x2 - x1)
    x2_ = c * x1 - x2 - 20 * x1 * x3  # c -> r
    x3_ = 5 * x1 * x2 - b * x3
    return x1_ * h, x2_ * h, x3_ * h


def slave1(x1, x2, x3, h):
    global a, b, c, d, k
    x1_ = a * (x2 - x1)
    x3_ = 5 * x1 * x2 - b * x3
    return x1_ * h, x2 * h, x3_ * h


def slave2(x1, x2, x3, h):
    global a, b, c, d, k
    x2_ = c * x1 - x2 - 20 * x1 * x3
    x3_ = 5 * x1 * x2 - b * x3
    return x1 * h, x2_ * h, x3_ * h


def synchro(x1, x2, x3, x4, x01, x02, x03, x04, x11, x12, x13, x14, iters=1000, h=0.01):
    """
    Apply Runge Kutta 4 for getting the values
    """
    xs, ys, zs = [], [], []
    x0s, y0s, z0s = [], [], []
    x1s, y1s, z1s = [], [], []
    for i in range(1, iters + 1):
        xs.append(x1)
        ys.append(x2)
        zs.append(x3)

        x0s.append(x01)
        y0s.append(x02)
        z0s.append(x03)

        x1s.append(x11)
        y1s.append(x12)
        z1s.append(x13)

        a1, a2, a3 = lorentz(x1, x2, x3, h)
        b1, b2, b3 = lorentz(x1 + a1 / 2, x2 + a2 / 2, x3 + a3 / 2, h)
        c1, c2, c3 = lorentz(x1 + b1 / 2, x2 + b2 / 2, x3 + b3 / 2, h)
        d1, d2, d3 = lorentz(x1 + c1, x2 + c2, x3 + c3, h)
        x1 = x1 + (a1 + 2 * b1 + 2 * c1 + d1) / 6
        x2 = x2 + (a2 + 2 * b2 + 2 * c2 + d2) / 6
        x3 = x3 + (a3 + 2 * b3 + 2 * c3 + d3) / 6

        a1, a2, a3 = slave1(x01, x2, x03, h)
        b1, b2, b3 = slave1(x01 + a1 / 2, x2 + a2 / 2, x03 + a3 / 2, h)
        c1, c2, c3 = slave1(x01 + b1 / 2, x2 + b2 / 2, x03 + b3 / 2, h)
        d1, d2, d3 = slave1(x01 + c1, x2 + c2, x03 + c3, h)
        x01 = x01 + (a1 + 2 * b1 + 2 * c1 + d1) / 6
        x02 = x02 + (a2 + 2 * b2 + 2 * c2 + d2) / 6
        x03 = x03 + (a3 + 2 * b3 + 2 * c3 + d3) / 6

        a1, a2, a3 = slave2(x11, x2, x13, h)
        b1, b2, b3 = slave2(x11 + a1 / 2, x2 + a2 / 2, x13 + a3 / 2, h)
        c1, c2, c3 = slave2(x11 + b1 / 2, x2 + b2 / 2, x13 + b3 / 2, h)
        d1, d2, d3 = slave2(x11 + c1, x2 + c2, x13 + c3, h)
        x11 = x01 + (a1 + 2 * b1 + 2 * c1 + d1) / 6
        x12 = x12 + (a2 + 2 * b2 + 2 * c2 + d2) / 6
        x13 = x13 + (a3 + 2 * b3 + 2 * c3 + d3) / 6

    return xs, ys, zs, x0s, y0s, z0s, x1s, y1s, z1s


def cipher(msg, st, iters, initial):
    xs, ys, zs, x0s, y0s, z0s, x1s, y1s, z1s = synchro(
        *initial, iters
    )

    # this initial state work perfectly
    # iters = 3000
    # st = 1000
    # xs, ys, zs, x0s, y0s, z0s, x1s, y1s, z1s = synchro(
    #     10, 10, 10, -10, 15, 15, 15, 15, 1, 1, 1, 1, iters
    # )

    aa = 0
    # Plot the surface.
    fig = plt.figure(1)
    ax = fig.gca(projection="3d")

    surf1 = ax.plot(
        np.array(xs[aa:]), np.array(ys[aa:]), np.array(zs[aa:]), c="r", label="lorentz"
    )
    # surf2 = ax.plot(
    #     np.array(x0s[aa:]),
    #     np.array(y0s[aa:]),
    #     np.array(z0s[aa:]),
    #     c="b",
    #     label="slave1",
    # )
    diff_e = np.average(np.array(y1s[aa:])-np.array(ys[aa:]))
    # y1s[aa:] = [x - diff_e for x in y1s[aa:]]
    surf3 = ax.plot(
        np.array(x1s[aa:]),
        np.array([x - diff_e for x in y1s[aa:]]),
        np.array(z1s[aa:]),
        c="g",
        label="slave2",
    )
    fig = plt.figure(2)

    dep = [_ for _ in range(len(x1s[aa:]))]
    plt.plot(dep, xs[aa:], c="b")
    plt.plot(dep, x0s[aa:], c="r")
    plt.plot(dep, [x + 0 for x in x1s[aa:]], c="g")
    fig = plt.figure(2)

    plt.plot(dep, ys[aa:], c="b")
    # plt.plot(dep, y0s[aa:], c="r")
    plt.plot(dep, [x - 62 for x in y1s[aa:]], c="g")

    fig = plt.figure(2)

    plt.plot(dep, zs[aa:], c="b")
    plt.plot(dep, z0s[aa:], c="r")
    plt.plot(dep, [x for x in z1s[aa:]], c="g")

    cy = ""
    for ch in msg:
        cx = int(ord(ch) ^ int(zs[st] + xs[st] + ys[st])) % 255
        cy += chr(cx) + ""
        st + 1
    plt.show()
    return cy


if __name__ == "__main__":
    initial = [10, 10, 10, -10, 15, 15, 15, 15, 1, 1, 1, 1]
    ciphered = cipher(msg="bghocj&ughriu", st=1000,
                      iters=1200, initial=initial)
    print("Ciphered message = {}".format(ciphered))
