import numpy as np


class ValueMapper:

    def __init__(self):
        # For 100K predefined resistors
        self.perBit = 5 / 1024
        # Some basic value pairs [voltage, gram]
        self.mapping100k = np.array([
            [0.0, 0],
            [2.5, 10],
            [3.55, 12],
            [4, 50],
            [4.2, 100],
            [4.45, 200],
            [4.5, 310],
            [4.6, 450],
            [4.65, 580],
            [4.75, 710],
            [4.8, 900],
            [4.85, 1000]])

        self.mapping10k = np.array([
            [0.0, 0],
            [0.9, 12],
            [1.4, 50],
            [1.8, 100],
            [2.2, 200],
            [2.5, 310],
            [2.8, 450],
            [3.0, 580],
            [3.2, 710],
            [3.35, 900],
            [3.4, 1000]])

    def get_mapped_value(self, value):
        toMap = [row[1] for row in value]
        # print("Coming in: {0}".format(toMap))
        toMap = [self.map_value(value, self.mapping10k) for value in toMap]
        # print("Going Out: {0}".format(toMap))
        return np.transpose(np.array([[row[0] for row in value], toMap]))

    def map_value(self, value, mapping):
        for i in range(len(mapping)-1):
            valueInvoltage = value*self.perBit
            if valueInvoltage >= mapping[i][0] and valueInvoltage < mapping[i+1][0]:
                # print("in range: {0} and {1} = {2}".format(mapping[i][0], mapping[i + 1][0], valueInvoltage))
                x1 = mapping[i][0]
                x2 = mapping[i + 1][0]
                y1 = mapping[i][1]
                y2 = mapping[i + 1][1]
                return y1 + ((valueInvoltage - x1)*(y2 - y1))/(x2-x1)
            # print("Not: {0} voltage: {1}".format(value, valueInvoltage))
        return value
