import os
import numpy as np
import math
from audio2numpy import open_audio
from operator import itemgetter
import matplotlib.pyplot as plt
from scipy.signal import correlate
import json

def get_directories(path='.'):
    return [entry.name for entry in os.scandir(path) if entry.is_dir()]


def getlocation(dirname):
    locationsplit=dirname.split("_")
    PosX=float(locationsplit[3])
    PosY=float(locationsplit[4])
    PosZ=float(locationsplit[5])
    Orien=float(locationsplit[7])
    return [PosX,PosY,PosZ,Orien]

def getdirname(dirlocation):
    cubeubication="Ubication_"+str(dirlocation[0])+"_"+str(dirlocation[1])+"_"+str(dirlocation[2])
    cubeorientation="Orientation_"+str(dirlocation[3])
    dirname="Position__"+cubeubication+"_"+cubeorientation
    return dirname

def euclidistance(location1, location2):
    deltaX=location1[0]-location2[0]
    deltaY=location1[1]-location2[1]
    deltaZ=location1[2]-location2[2]
    return math.sqrt(deltaX**2+deltaY**2+deltaZ**2)

def orderbydistance(dirref, dirlist):
    dirplusdis=[]
    for dir in dirlist:
        distance=euclidistance(getlocation(dirref),getlocation(dir))
        dirplusdis.append([dir,distance])
    orderlist=sorted(dirplusdis,key=itemgetter(1))
    return orderlist




signals_path='C:/Users/Esteban/python_code/Recordings/New_ARM/Session3'

samplerate = 44100
#moverse al directorio
os.chdir(signals_path)
#obtener los directorios de las senales
directories = get_directories(signals_path)

#print(directories[1])
#print(getlocation(directories[1]))
#print(getlocation(directories[10]))
#print(getdirname(getlocation(directories[1])))
#print(euclidistance(getlocation(directories[1]),getlocation(directories[10])))
#print(orderbydistance(directories[1],directories[1:40]))

cross_corrArray=[]
origin=directories[0]
orderedfromOrigin=orderbydistance(origin,directories)
countrefpoints=1
for refpointext in orderedfromOrigin:
    refpoint=refpointext[0]
    print("cross correlation for signal:"+ str(countrefpoints))
    orderedfromrefpoint=orderbydistance(refpoint,directories)
    cross_ordpoints=[]
    refch1_point,sample_rate1 = open_audio(refpoint+"/aligned_channel2.wav")

    for point in orderedfromrefpoint:
        chn1_point, sample_rate2 = open_audio(point[0]+"/aligned_channel2.wav")
        #cross_corr = np.correlate(refch1_point,chn1_point, mode='full')
        cross_corr = correlate(refch1_point,chn1_point, mode='full')
        max_val=np.max(cross_corr)
        cross_ordpoints.append([point[0],point[1],float(max_val)])
    
    signal=countrefpoints
    distances=[sublist[1] for sublist in cross_ordpoints]
    xcorrelation=[sublist[2] for sublist in cross_ordpoints]
    cross_corrArray.append([signal,distances,xcorrelation])
    countrefpoints=countrefpoints+1


with open('xcorrArray.json', 'w') as file:
    json.dump(cross_corrArray, file)



#plt.plot(distances, xcorrelation, color='purple', linestyle='--', marker='s', linewidth=2, markersize=8)
#plt.title("cross correlation vs distance")
#plt.xlabel("distance between points")
#plt.ylabel("cross correlation of signals")
#plt.show()



