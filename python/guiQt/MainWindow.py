from PyQt4 import QtGui  # (the example applies equally well to PySide)
import pyqtgraph as pg
import numpy as np

from python.guiQt.StartWindow import StartWindow


class Gui(QtGui.QMainWindow):

    measurementValuesProcessor = None
    yValues = []
    xValues = []
    curves = []
    pens = ['r', 'g', 'b', 'c']
    numberShownPoints = 100

    def __init__(self, measurementValuesProcessor):
        QtGui.QMainWindow.__init__(self)
        self.measurementValuesProcessor = measurementValuesProcessor
        self.mw = StartWindow(measurementValuesProcessor)
        self.show()
        self.mw.show()
