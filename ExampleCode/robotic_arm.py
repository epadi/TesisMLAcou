from pymycobot.mycobot280 import MyCobot280
import time

def getlocation(coordenadas):
  xcord=coordenadas[0]/10
  ycord=coordenadas[1]/10
  zcord=((coordenadas[2]-180)/10)*1.17

  xrot=coordenadas[3]
  yrot=coordenadas[4]
  zrot=coordenadas[5]

  print("")
  print("Coordenadas (cm):")
  print("X="+f"{xcord:.2f}")
  print("Y="+f"{ycord:.2f}")
  print("Z="+f"{zcord:.2f}")
  print("")
  print("Orientacion (grados):")
  print("rotaX="+f"{xrot:.2f}")
  print("rotaY="+f"{yrot:.2f}")
  print("rotaZ="+f"{zrot:.2f}")
  print("")
  result=[xcord,ycord,zcord,xrot,yrot,zrot]
  return result

def wait4location(seg):
  for i in range(1,seg):
    print("wait "+str(i)+"s/"+ str(seg)+"s")
    time.sleep(1)

mc = MyCobot280("COM6", 115200)
if mc.get_fresh_mode() != 1:
  mc.set_fresh_mode(1)

#posicion inicial
#mc.send_angles([0,0,0,0,0,160], 3)

#wait4location(20)

#Obtener ubicacion
angles=mc.get_angles()
print(angles)
coords=mc.get_coords()
getlocation(coords)


#round1 
#1) swap axis 6 -160->160 
#2) swap axis 2    0->130
#3) swap axis 1 -160->160

wait4location(20)
mc.send_angles([-2.28, -91.14, -74.17, 83.49, 0.35, -117.68], 3)






