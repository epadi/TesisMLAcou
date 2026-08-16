import os
import numpy as np
import math
from audio2numpy import open_audio
from operator import itemgetter
import matplotlib.pyplot as plt


def getsignalpower(directory, channel):
    signal,sample_rate = open_audio(directory+"/"+channel)
    power = np.mean(signal**2)
    return power

def get_directories(path='.'):
    return [entry.name for entry in os.scandir(path) if entry.is_dir()]


signals_path='C:/Users/Esteban/python_code/Recordings/New_ARM/Session1/Position__Ubicacion_-261.6419667_-10.03876553_412.3882604_Orientacion_120'


sigpower_ch2=getsignalpower(signals_path,"aligned_channel2.wav")
print("CH2 power:"+str(sigpower_ch2))
