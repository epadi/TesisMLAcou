import os
import numpy as np
import math
from audio2numpy import open_audio
from operator import itemgetter
import matplotlib.pyplot as plt
from scipy.signal import correlate
import json


def normalized_cross_correlation(signal1, signal2):
    signal1 = np.asarray(signal1).squeeze()
    signal2 = np.asarray(signal2).squeeze()
    signal1 = signal1 - np.mean(signal1)
    signal2 = signal2 - np.mean(signal2)
    denominator = np.linalg.norm(signal1) * np.linalg.norm(signal2)
    if denominator == 0:
        return 0.0
    return float(np.max(correlate(signal1, signal2, mode='full')) / denominator)



reference_path='C:/Users/Esteban/TesisCode/Recordings/WW27_Rec/S26/'
directory_name='Position__Ubicacion_90.33688561_216.2139435_9.314473701_Orientacion_'
reference_signal_path=os.path.join(reference_path, directory_name)


signal_same_orientation_paths=[]
channel="aligned_channel1.wav"
samplerate = 44100
orientations=[50,60,70,80,90,100,110,120,130]

signal_cross_ordpoints=[]
ref_signal, samplerate = open_audio(reference_signal_path+"50/"+channel)
for orientation in orientations:
    signal,samplerate = open_audio(reference_signal_path+str(orientation)+"/"+channel)
    signal_cross_ordpoints.append(normalized_cross_correlation(ref_signal, signal))


plt.plot(orientations, signal_cross_ordpoints, color='purple', linestyle='--', marker='s', linewidth=2, markersize=8)
plt.title("normalized cross correlation vs orientation")
plt.xlabel("orientation (degrees)")
plt.ylabel("normalized cross-correlation coefficient")
plt.show()


