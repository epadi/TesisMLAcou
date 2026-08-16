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


signals_path='C:/Users/Esteban/python_code/Recordings/WW27_Rec/Test_sessions/S0.4'
os.chdir(signals_path)

directories=get_directories(signals_path)
countinv_ch1=0
countinv_ch2=0
countinv_ch3=0
countinv_ch4=0
channelcorrupted=False

for directory in directories:
    sigpower_ch1=getsignalpower(directory,"aligned_channel1.wav")
    print("CH1 power:"+str(sigpower_ch1))
    sigpower_ch2=getsignalpower(directory,"aligned_channel2.wav")
    print("CH2 power:"+str(sigpower_ch2))
    sigpower_ch3=getsignalpower(directory,"aligned_channel3.wav")
    print("CH3 power:"+str(sigpower_ch3))
    sigpower_ch4=getsignalpower(directory,"aligned_channel4.wav")
    print("CH4 power:"+str(sigpower_ch4))

    channelcorrupted=False
    if sigpower_ch1<0.001 or math.isnan(sigpower_ch1):
        print("On Measurement " + directory+ " channel1 is invalid")
        countinv_ch1=countinv_ch1+1
        channelcorrupted=True
    if sigpower_ch2<0.001 or math.isnan(sigpower_ch2):
        print("On Measurement " + directory+ " channel2 is invalid")
        countinv_ch2=countinv_ch2+1
        channelcorrupted=True
    if sigpower_ch3<0.001 or math.isnan(sigpower_ch3):
        print("On Measurement " + directory+ " channel3 is invalid")
        countinv_ch3=countinv_ch3+1
        channelcorrupted=True
    if sigpower_ch4<0.001 or math.isnan(sigpower_ch4):
        print("On Measurement " + directory+ " channel4 is invalid")
        countinv_ch4=countinv_ch4+1
        channelcorrupted=True
    
    if channelcorrupted==False:
        print("On Measurement " + directory+ " ALL CHANNELS ARE PASSING")


print("total invalids for ch1="+ str(countinv_ch1))
print("total invalids for ch2="+ str(countinv_ch2))
print("total invalids for ch3="+ str(countinv_ch3))
print("total invalids for ch4="+ str(countinv_ch4))




