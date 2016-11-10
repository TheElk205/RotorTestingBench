#!/usr/bin/python3
from python.guiQt.Gui import Gui
from python.guiQt.MeasurementValuesProcessor import MeasurementValuesProcessor

import os
prefixed = [filename for filename in os.listdir('/dev') if filename.startswith("ttyACM")]
print("Available Android Devices: {0}".format(prefixed))

measurementValuesProcessor = MeasurementValuesProcessor('/dev/' + prefixed[0])
gui = Gui(measurementValuesProcessor)