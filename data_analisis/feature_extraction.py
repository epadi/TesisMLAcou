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


def smoothsignal(signal, nval):
    smooth_signal=[]
    for x in range(0,len(signal)-nval):
        prominterval=0
        for i in range(0,nval):
            prominterval=prominterval+signal[x+i][1]
        smooth_signal.append([signal[x][0],prominterval/nval])
    return smooth_signal


def getsignalenvolv(directory, channel):
    signal,sample_rate = open_audio(directory+"/"+channel)
    max_mins=[]
    previous_val=0
    for index in range(1,len(signal)-1):
        diff_prev=signal[index]-signal[index-1]
        diff_post=signal[index+1]-signal[index]
        if diff_prev>0 and diff_post<0 :
            max_mins.append([index,abs(signal[index])])
        if diff_prev<0 and diff_post>0 :
            max_mins.append([index,abs(signal[index])])

    smoothsig=smoothsignal(max_mins,100)
    return smoothsig


def getlensignal(signal):
    checkforpoint1=True
    checkforpoint2=False
    checkforpoint3=False
    for x in range(0,len(signal)):
        if checkforpoint1==True and signal[x][1]>0.1:
            signal_point1=signal[x][0]
            checkforpoint1=False
            checkforpoint2=True
        if checkforpoint2==True and signal[x][1]<0.1:
            signal_point2=signal[x][0]
            checkforpoint2=False
            checkforpoint3=True
        if checkforpoint3==True and signal[x][1]<0.05:
            signal_point3=signal[x][0]
            checkforpoint3=False
                
    body=signal_point2-signal_point1
    tail=signal_point3-signal_point2

    return [body, tail]




signals_path='C:/Users/Esteban/python_code/Recordings/New_ARM/Session2'
os.chdir(signals_path)
sigpower=getsignalpower("Position__Ubicacion_-243.6359373_-34.99488205_381.5777052_Orientacion_90","aligned_channel2.wav")
print(sigpower)

signalenvolv=getsignalenvolv("Position__Ubicacion_-243.6359373_-34.99488205_381.5777052_Orientacion_90","aligned_channel2.wav")

print(getlensignal(signalenvolv))

#print(signalenvolv)
x = np.array([sublist[0] for sublist in signalenvolv])
y = np.array([sublist[1] for sublist in signalenvolv])

plt.plot(x, y, color='purple', linestyle='--', marker='s', linewidth=2, markersize=8)
plt.title("cross correlation vs distance")
plt.xlabel("distance between points")
plt.ylabel("cross correlation of signals")
plt.show()


