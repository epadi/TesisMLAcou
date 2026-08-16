import os
import numpy as np
import math
from audio2numpy import open_audio
from operator import itemgetter
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
from matplotlib.colors import LinearSegmentedColormap


signals_path='C:/Users/Esteban/python_code/Recordings/New_ARM/Session2'
os.chdir(signals_path)

plotdefine="xcorr2D"

with open('xcorrArray.json', 'r') as file:
    cross_corrArray = json.load(file)





dataxcor3D=[]
for entry in cross_corrArray:
    for element in range(len(entry[1])):
        dataxcor3D.append([entry[1][element],entry[0],entry[2][element]])

#2D plot
if plotdefine=="xcorr2D":
    signal=cross_corrArray[0][0]
    distances=cross_corrArray[0][1]
    xcorrelation=cross_corrArray[0][2]
    plt.plot(distances, xcorrelation, color='purple', linestyle='--', marker='s', linewidth=2, markersize=8)
    plt.title("cross correlation vs distance")
    plt.xlabel("distance between points")
    plt.ylabel("cross correlation of signals")
    plt.show()


#3D Plot
if plotdefine=="xcorr3D":
    x = np.array([sublist[0] for sublist in dataxcor3D])
    y = np.array([sublist[1] for sublist in dataxcor3D])
    z = np.array([sublist[2] for sublist in dataxcor3D])
    X, Y = np.meshgrid(x, y)
    Z = z
    custom_cmap = LinearSegmentedColormap.from_list("custom", ["darkblue", "skyblue", "yellow", "red"])
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_trisurf(x, y, z, cmap=custom_cmap)
    fig.colorbar(surf)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.legend()
    plt.show()


