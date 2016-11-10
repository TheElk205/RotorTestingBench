import numpy as np


class ValueMapper:

    def __init__(self):
        None

    def get_mapped_value(self, value):
        toMap = [row[1] for row in value]
        # print("Coming in: {0}".format(toMap))
        toMap = [value * 0.01 for value in toMap]
        # print("Going Out: {0}".format(toMap))
        return np.transpose(np.array([[row[0] for row in value], toMap]))

    def map_value(self, value):
        return value*0.001
