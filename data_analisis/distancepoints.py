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






signals1_path='C:/Users/Esteban/python_code/Recordings/New_ARM/Session1/Position__Ubicacion_-246.6097453_-9.462004284_-130.5141637_Orientacion_50'
signals2_path='C:/Users/Esteban/python_code/Recordings/New_ARM/Session2/Position__Ubicacion_-227.9711053_-32.74484885_-134.6839718_Orientacion_50'


loc1=getlocation('Position__Ubicacion_-246.6097453_-9.462004284_-130.5141637_Orientacion_50')
loc2=getlocation('Position__Ubicacion_-227.9711053_-32.74484885_-134.6839718_Orientacion_50')

print(euclidistance(loc1,loc2))
