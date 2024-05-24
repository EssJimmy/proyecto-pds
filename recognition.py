#import pyaudio
#import wave
import sys
#from scipy.io import wavfile
from scipy.signal import butter, lfilter
import numpy as np
from matplotlib import pyplot as plt
import librosa

# function should return a string that represents the
# words that it understood
# so far this is a pseudo implementation on how the code
# shoud work
def recognition(file_name: str, key_file_name: str) -> bool:
    filtered_attempt = read_wav(file_name)
    filtered_key = read_wav(key_file_name)

    S1, phase1 = librosa.magphase(librosa.stft(filtered_attempt))
    S2, phase2 = librosa.magphase(librosa.stft(filtered_key))

    rms1 = librosa.feature.rms(S=S1)
    rms2 = librosa.feature.rms(S=S2)

    mse = (rms1[0]-rms2[0])**2
    mse = sum(mse)

    print(mse)

    return mse < 0.01


def read_wav(file_name: str):
    data, sr = librosa.load(file_name)
    return filter(sr, data, 500, 1)


def filter(sr: int, data: np.array, cutoff: int, order: int) -> np.array:
    b, a = butter(order, cutoff, btype='low', analog=False, output='ba', fs=2*sr)
    y = lfilter(b, a, data)
    return y


def main():
    audio_1 = "output1.wav"
    audio_2 = "output2.wav"

    recognition("login_attempt1.wav", audio_2)


if __name__ == '__main__':
    main()

