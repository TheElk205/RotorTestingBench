#!/usr/bin/python3
from python.guiQt.MainWindow import Gui
from PyQt4 import QtGui
from python.guiQt.MeasurementValuesProcessor import MeasurementValuesProcessor

import os

from python.guiQt.SerialCommunicator import SerialCommunicator

prefixed = [filename for filename in os.listdir('/dev') if filename.startswith("ttyACM")]
print("Available Android Devices: {0}".format(prefixed))

serialCommunicator = SerialCommunicator('/dev/' + prefixed[0])
measurementValuesProcessor = MeasurementValuesProcessor(serialCommunicator)

## Always start by initializing Qt (only once per application)
app = QtGui.QApplication([])

gui = Gui(measurementValuesProcessor, serialCommunicator, None)
## Start the Qt event loop
app.exec_()
