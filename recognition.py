import pyaudio
import wave
import sys
from scipy.io import wavfile
from scipy.signal import butter, lfilter
import numpy as np
from matplotlib import pyplot as plt

# function should return a string that represents the
# words that it understood
# so far this is a pseudo implementation on how the code
# shoud work
def recognition(file_name: str, key_file_name: str) -> bool:
    filtered_attempt = read_wav(file_name)
    filtered_key = read_wav(key_file_name)

    return filtered_key == filtered_attempt # this is just temporary


def read_wav(file_name: str):
    sr, data = wavfile.read(file_name)
    return filter(sr, data, 500, 1)


def filter(sr: int, data: np.array, cutoff: int, order: int) -> np.array:
    b, a = butter(order, cutoff, btype='low', analog=False, output='ba', fs=2*sr)
    y = lfilter(b, a, data)
    return y


def main():
    filtered_data = read_wav('login_attempt1_wav')
    plt.plot(filtered_data)
    plt.show()


if __name__ == '__main__':
    main()

