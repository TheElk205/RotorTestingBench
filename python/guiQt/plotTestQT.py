# -*- coding: utf-8 -*-

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

from python.guiQt.SerialReader import SerialReader

win = pg.GraphicsWindow()
win.setWindowTitle('pyqtgraph example: Scrolling Plots')

numberShownPoints = 100

plots = []
yValues = []
xValues = []
curves = []
pens = ['r', 'g', 'b', 'c']
for i in range(0, 4):
    if i == 2:
        win.nextRow()
    if i == 0:
        plots.append(win.addPlot())
    yValues.append(np.zeros(shape=numberShownPoints))
    xValues.append(np.zeros(shape=numberShownPoints))
    curves.append(plots[0].plot(yValues[i], pen=pens[i]))

threads = []

serialReader = SerialReader(1, "Thread-1", 1)

serialReader.start()

threads.append(serialReader)


def update1():
    global yValues, curves
    for ii in range(0, 4):
        timeValuePairs = np.array(serialReader.values[ii])
        if timeValuePairs.size > 2:
            yValues[ii] = timeValuePairs[:, 1]
            xValues[ii] = timeValuePairs[:, 0]
            if yValues[ii].size > numberShownPoints:
                curves[ii].setData(y=yValues[ii][-numberShownPoints:], x=xValues[ii][-numberShownPoints:])
                curves[ii].setPos(yValues[ii].size - numberShownPoints, 0)
            else:
                curves[ii].setData(y=yValues[ii], x=xValues[ii])
                curves[ii].setPos(0, 0)


# update all plots
def update():
    update1()


timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(20)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
