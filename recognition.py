import pyaudio
import wave
import sys
from scipy.io import wavfile
from scipy.signal import butter, lfilter
import numpy as np
from matplotlib import pyplot as plt

# function should return a string that represents the
# words that it understood
def recognition(file_name: str) -> str:
    pass


def test(file_name: str):
    sr, data = wavfile.read(file_name)
    return data, filter(sr, data, 500, 1)


def filter(sr: int, data: np.array, cutoff: int, order: int) -> np.array:
    b, a = butter(order, cutoff, btype='low', analog=False, output='ba', fs=2*sr)
    y = lfilter(b, a, data)
    return y


def main():
    _, f = test('login_attempt1.wav')
    plt.plot(f[1:400], 'b')
    plt.show()


if __name__ == '__main__':
    main()

