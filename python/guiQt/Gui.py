from PyQt4 import QtGui  # (the example applies equally well to PySide)
import pyqtgraph as pg
import numpy as np

class Gui:

    measurementValuesProcessor = None
    yValues = []
    xValues = []
    curves = []
    pens = ['r', 'g', 'b', 'c']
    numberShownPoints = 100

    def __init__(self, measurementValuesProcessor):
        self.measurementValuesProcessor = measurementValuesProcessor

        ## Always start by initializing Qt (only once per application)
        app = QtGui.QApplication([])

        ## Define a top-level widget to hold everything
        w = QtGui.QWidget()

        ## Create some widgets to be placed inside
        btn = QtGui.QPushButton('press me')
        btn.clicked.connect(self.test)
        text = QtGui.QLineEdit('enter text')
        listw = QtGui.QListWidget()
        plot = pg.PlotWidget()

        ## Create a grid layout to manage the widgets size and position
        layout = QtGui.QGridLayout()
        w.setLayout(layout)

        ## Add widgets to the layout in their proper positions
        layout.addWidget(btn, 0, 0)   # button goes in upper-left
        layout.addWidget(text, 1, 0)   # text edit goes in middle-left
        layout.addWidget(listw, 2, 0)  # list widget goes in bottom-left
        layout.addWidget(plot, 0, 1, 3, 1)  # plot goes on right side, spanning 3 rows

        for i in range(0, 4):
            self.yValues.append(np.zeros(shape=self.numberShownPoints))
            self.xValues.append(np.zeros(shape=self.numberShownPoints))
            self.curves.append(plot.plot(self.yValues[i], pen=self.pens[i]))

        ## Add timer for updating the display
        timer = pg.QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(20)

        ## Display the widget as a new window
        w.show()

        ## Start the Qt event loop
        app.exec_()

    def update(self):
        global yValues, curves, numberShownPoints, xValues
        for ii in range(0, 4):
            timeValuePairs = np.array(self.measurementValuesProcessor.get_last_n_values(self.numberShownPoints)[ii])
            if timeValuePairs.size > 2:
                self.yValues[ii] = timeValuePairs[:, 1]
                self.xValues[ii] = timeValuePairs[:, 0]
                if self.yValues[ii].size > self.numberShownPoints:
                    self.curves[ii].setData(y=self.yValues[ii][-self.numberShownPoints:], x=self.xValues[ii][-self.numberShownPoints:])
                    self.curves[ii].setPos(self.yValues[ii].size - self.numberShownPoints, 0)
                else:
                    self.curves[ii].setData(y=self.yValues[ii], x=self.xValues[ii])
                    self.curves[ii].setPos(0, 0)

    def test(self):
        print("Test")
