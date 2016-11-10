import numpy as np
from PyQt4 import QtGui

from PyQt4.QtGui import QWidget


class StartWindow(QWidget):
    def __init__(self, measurementValuesProcessor, *args):
        QWidget.__init__(self, *args)

        ## Create some widgets to be placed inside
        self.measurementValuesProcessor = measurementValuesProcessor
        self.btn = QtGui.QPushButton('press me')
        # self.btn.clicked.connect(self.test)
        self.text = QtGui.QLineEdit('enter text')
        self.listw = QtGui.QListWidget()
        self.plot = self.PlotWidget()

        ## Create a grid layout to manage the widgets size and position
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        ## Add widgets to the layout in their proper positions
        self.layout.addWidget(self.btn, 0, 0)  # button goes in upper-left
        self.layout.addWidget(self.text, 1, 0)  # text edit goes in middle-left
        self.layout.addWidget(self.listw, 2, 0)  # list widget goes in bottom-left
        self.layout.addWidget(self.plot, 0, 1, 3, 1)  # plot goes on right side, spanning 3 rows

        for i in range(0, 4):
            self.yValues.append(np.zeros(shape=self.numberShownPoints))
            self.xValues.append(np.zeros(shape=self.numberShownPoints))
            self.curves.append(self.plot.plot(self.yValues[i], pen=self.pens[i]))

        ## Add timer for updating the display
        timer = self.QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(20)


    def update(self):
        global yValues, curves, numberShownPoints, xValues
        for ii in range(0, 4):
            timeValuePairs = np.array(self.measurementValuesProcessor.get_last_n_values(self.numberShownPoints)[ii])
            if timeValuePairs.size > 2:
                self.yValues[ii] = timeValuePairs[:, 1]
                self.xValues[ii] = timeValuePairs[:, 0]
                print("Values to visualize: {0}".format(self.yValues[ii].size))
                if self.yValues[ii].size > self.numberShownPoints:
                    self.curves[ii].setData(y=self.yValues[ii][-self.numberShownPoints:],
                                            x=self.xValues[ii][-self.numberShownPoints:])
                    self.curves[ii].setPos(self.yValues[ii].size - self.numberShownPoints, 0)
                else:
                    self.curves[ii].setData(y=self.yValues[ii], x=self.xValues[ii])
                    self.curves[ii].setPos(0, 0)
