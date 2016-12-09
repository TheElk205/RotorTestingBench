from PyQt4 import QtGui  # (the example applies equally well to PySide)
import pyqtgraph as pg
import numpy as np
from PyQt4.QtGui import QSlider

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Gui(QtGui.QWidget):
    maxPwm = 100;
    yValues = []
    xValues = []
    curves = []
    pens = ['r', 'g', 'b', 'c']
    numberShownPoints = 100
    serialCommunicator = None

    def __init__(self, measurementValuesProcessor, serialCommunicator, *args):
        QtGui.QWidget.__init__(self, *args)
        self.measurementValuesProcessor = measurementValuesProcessor
        self.serialCommunicator = serialCommunicator
        ## Create some widgets to be placed inside
        self.measurementValuesProcessor = measurementValuesProcessor
        # self.btn = QtGui.QPushButton('press me')
        # self.btn.clicked.connect(self.test)
        # self.text = QtGui.QLineEdit('enter text')
        # self.listw = QtGui.QListWidget()
        self.sl = QSlider(Qt.Horizontal)
        self.sl.setMinimum(0)
        self.sl.setMaximum(self.maxPwm)
        self.sl.setValue(0)
        self.slText = QtGui.QLineEdit('0')
        self.sl.valueChanged.connect(self.motorSliderChanged)

        self.plot = pg.PlotWidget()

        ## Create a grid layout to manage the widgets size and position
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        ## Add widgets to the layout in their proper positions
        # self.layout.addWidget(self.btn, 0, 0)  # button goes in upper-left
        # self.layout.addWidget(self.text, 1, 0)  # text edit goes in middle-left
        # self.layout.addWidget(self.listw, 2, 0)  # list widget goes in bottom-left
        self.layout.addWidget(self.sl, 0, 0)
        self.layout.addWidget(self.slText, 1, 0)
        self.layout.addWidget(self.plot, 0, 1)  # plot goes on right side, spanning 3 rows

        for i in range(0, 4):
            self.yValues.append(np.zeros(shape=self.numberShownPoints))
            self.xValues.append(np.zeros(shape=self.numberShownPoints))
            self.curves.append(self.plot.plot(self.yValues[i], pen=self.pens[i]))

        ## Add timer for updating the display
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(20)

        self.show()

    def update(self):
        global yValues, curves, numberShownPoints, xValues
        for ii in range(0, 4):
            timeValuePairs = np.array(self.measurementValuesProcessor.get_last_n_values(self.numberShownPoints)[ii])
            if timeValuePairs.size > 2:
                self.yValues[ii] = timeValuePairs[:, 1]
                self.xValues[ii] = timeValuePairs[:, 0]
                if self.yValues[ii].size > self.numberShownPoints:
                    self.curves[ii].setData(y=self.yValues[ii][-self.numberShownPoints:],
                                            x=self.xValues[ii][-self.numberShownPoints:])
                    self.curves[ii].setPos(self.yValues[ii].size - self.numberShownPoints, 0)
                else:
                    self.curves[ii].setData(y=self.yValues[ii], x=self.xValues[ii])
                    self.curves[ii].setPos(0, 0)

    def closeEvent(self, event):
        self.measurementValuesProcessor.stop_serial()

    def motorSliderChanged(self, value):
        print("Slider value: {0}".format(value))
        self.slText.setText("{0}".format(value))
        self.serialCommunicator.send_bytes_to_serial(value)