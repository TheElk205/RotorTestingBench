# -*- coding: utf-8 -*-
"""
Various methods of drawing scrolling plots.
"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

from python.guiQt.SerialReader import SerialReader

win = pg.GraphicsWindow()
win.setWindowTitle('pyqtgraph example: Scrolling Plots')

numberShownPoints = 50

plots = []
data = []
curves = []
for i in range(0, 4):
    if i == 2:
        win.nextRow()
    plots.append(win.addPlot())
    data.append(np.zeros(shape=numberShownPoints))
    curves.append(plots[i].plot(data[i]))

threads = []

serialReader = SerialReader(1, "Thread-1", 1)

serialReader.start()

threads.append(serialReader)


def update1():
    global data, curves
    for ii in range(0, 4):
        timeValuePairs = np.array(serialReader.values[ii])
        if timeValuePairs.size > 2:
            data[ii] = timeValuePairs[:, 1]
            if data[ii].size > numberShownPoints:
                curves[ii].setData(data[ii][-numberShownPoints:])
                curves[ii].setPos(data[ii].size - numberShownPoints, 0)
            else:
                curves[ii].setData(data[ii])
                curves[ii].setPos(0, 0)


# update all plots
def update():
    update1()


timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
