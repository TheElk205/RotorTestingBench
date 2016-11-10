#!/usr/bin/python3
from python.guiQt.MainWindow import Gui
from PyQt4 import QtGui
from python.guiQt.MeasurementValuesProcessor import MeasurementValuesProcessor

import os
prefixed = [filename for filename in os.listdir('/dev') if filename.startswith("ttyACM")]
print("Available Android Devices: {0}".format(prefixed))

measurementValuesProcessor = MeasurementValuesProcessor('/dev/' + prefixed[0])

## Always start by initializing Qt (only once per application)
app = QtGui.QApplication([])

gui = Gui(measurementValuesProcessor, None)
## Start the Qt event loop
app.exec_()
