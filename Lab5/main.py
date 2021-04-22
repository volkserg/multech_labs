from scipy.io import wavfile
import math
import numpy as np

def openwave(filename):
    fs, data = wavfile.read(filename)
    return data

class Mlaw:

    def __init__(self, data):
        self.myu = 255
        self.signal = data
        self.signal_normalized = []
        self.signal_myu_encoded = []
        self.normalize_signal()
        self.myu_encode()

    def normalize_signal(self):
        absolute_arr = []

        for item in self.signal:
            absolute_arr.append(abs(item))

        max_val = np.amax(absolute_arr)
        result = []

        for item in self.signal:
            result.append(item / max_val)

        self.signal_normalized = result

    def sgn(self, x):
        return 1 if x > 0 else -1

    def myu_encode(self):
        for item in self.signal_normalized:
            self.signal_myu_encoded.append(self.__myu_encode(item))

    def __myu_encode(self, x):
        sgn_x = self.sgn(x)
        fraction = math.log(1 + self.myu * abs(x)) / math.log(1 + self.myu)

        return sgn_x * fraction


class Alaw:

    def __init__(self, data):
        self.a = 87.6
        self.signal = data
        self.signal_normalized = []
        self.signal_a_encoded = []
        self.normalize_signal()
        self.a_encode()

    def normalize_signal(self):
        absolute_arr = []

        for item in self.signal:
            absolute_arr.append(abs(item))

        max_val = np.amax(absolute_arr)
        result = []

        for item in self.signal:
            result.append(item / max_val)

        self.signal_normalized = result

    def sgn(self, x):
        return 1 if x > 0 else -1

    def a_encode(self):
        for item in self.signal_normalized:
            self.signal_a_encoded.append(self.__a_encode(item))

    def __a_encode(self, x):
        sgn_x = self.sgn(x)

        if(abs(x) < (1 / self.a)):
            fraction = self.a * abs(x) / (1 + math.log(self.a))
        else:
            fraction = (1 + math.log(self.a * abs(x))) / (1 + math.log(self.a))

        return sgn_x * fraction
