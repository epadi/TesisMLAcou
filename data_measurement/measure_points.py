import os
import numpy as np
import math
from audio2numpy import open_audio
from operator import itemgetter
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap


def get_directories(path='.'):
    return [entry.name for entry in os.scandir(path) if entry.is_dir()]

def getlocation(dirname):
    locationsplit=dirname.split("_")
    PosX=float(locationsplit[3])
    PosY=float(locationsplit[4])
    PosZ=float(locationsplit[5])
    Orien=float(locationsplit[7])
    return [PosX,PosY,PosZ,Orien]

signals_path='C:/Users/Esteban/python_code/Recordings/WW27_Rec/'



#moverse al directorio
os.chdir(signals_path)
#obtener los directorios de las senales
sessions = get_directories(signals_path)

measure_points=[]
for session in sessions:
    os.chdir(session)
    
    if session.find("S")!=-1:
        print(session)
        measures=get_directories(signals_path+session)
        for measure_point in measures:
            location=getlocation(measure_point)
            measure_points.append(location[0:3])
    os.chdir(signals_path)

x=[sublist[0] for sublist in measure_points]
y=[sublist[1] for sublist in measure_points]
z=[sublist[2] for sublist in measure_points]

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the points
ax.scatter(x, y, z, c=z, cmap='viridis', marker='o')
#ax.set_xlim(left=-300)
#ax.set_ylim(bottom=-300)
#ax.set_zlim(bottom=-300)
ax.set_xlim(-250, 250)   # X-axis range
ax.set_ylim(-250, 250)   # Y-axis range
ax.set_zlim(-300, 400)   # Z-axis range

ax.set_title("3D Scatter Plot")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis")

# Show the plot
plt.show()
