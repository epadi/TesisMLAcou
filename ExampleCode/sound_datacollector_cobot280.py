import pyaudio
import os
import time
import msvcrt
from playsound import playsound
from multiprocessing import Process
import wave
from pathlib import Path
import shutil
from pymycobot.mycobot280 import MyCobot280
from datetime import datetime

def getlocation(coordenadas):
  xcord=coordenadas[0]/10
  ycord=coordenadas[1]/10
  zcord=((coordenadas[2]-180)/10)*1.17

  xrot=coordenadas[3]
  yrot=coordenadas[4]
  zrot=coordenadas[5]

  Xcordstr=f"{xcord:.2f}"
  Ycordstr=f"{ycord:.2f}"
  Zcordstr=f"{zcord:.2f}"
  Xrotstr=f"{xrot:.2f}"
  Yrotstr=f"{yrot:.2f}"
  Zrotstr=f"{zrot:.2f}"
  print("")
  print("Coordenadas (cm):")
  print("X="+Xcordstr)
  print("Y="+Ycordstr)
  print("Z="+Zcordstr)
  print("")
  print("Orientacion (grados):")
  print("rotaX="+Xrotstr)
  print("rotaY="+Yrotstr)
  print("rotaZ="+Zrotstr)
  print("")
  result=[Xcordstr,Ycordstr,Zcordstr,Xrotstr,Yrotstr,Zrotstr]
  return result

def wait4location(seg):
  for i in range(1,seg):
    print("wait "+str(i)+"s/"+ str(seg)+"s")
    time.sleep(1)

def soundtrigger():
    #audio = Path().cwd() / "sound2.wav"
    audio = "C:/Users/Esteban/python_code/sound3.wav"
    playsound(audio)

def recordsound1():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 2
    OUTPUT_FILES = ["channel1.wav"]  # Output files for each microphone
    DEVICE_INDEXES = [2]  # Replace with your microphone device indexes

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open streams for each microphone
    streams = [
                audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=idx, frames_per_buffer=CHUNK)
                for idx in DEVICE_INDEXES
            ]

    print("Recording...")

    # Record audio
    frames = [[] for _ in DEVICE_INDEXES]
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        for i, stream in enumerate(streams):
            data = stream.read(CHUNK)
            frames[i].append(data)

    print("Finished recording.")

    # Save audio to files
    for i, frame in enumerate(frames):
        wf = wave.open(OUTPUT_FILES[i], 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frame))
        wf.close()

    # Close streams
    for stream in streams:
        stream.stop_stream()
        stream.close()
    audio.terminate()


def recordsound2():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 2
    OUTPUT_FILES = ["channel2.wav"]  # Output files for each microphone
    DEVICE_INDEXES = [5]  # Replace with your microphone device indexes

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open streams for each microphone
    streams = [
                audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=idx, frames_per_buffer=CHUNK)
                for idx in DEVICE_INDEXES
            ]

    print("Recording...")

    # Record audio
    frames = [[] for _ in DEVICE_INDEXES]
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        for i, stream in enumerate(streams):
            data = stream.read(CHUNK)
            frames[i].append(data)

    print("Finished recording.")

    # Save audio to files
    for i, frame in enumerate(frames):
        wf = wave.open(OUTPUT_FILES[i], 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frame))
        wf.close()

    # Close streams
    for stream in streams:
        stream.stop_stream()
        stream.close()
    audio.terminate()


def recordsound3():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 2
    OUTPUT_FILES = ["channel3.wav"]  # Output files for each microphone
    DEVICE_INDEXES = [1]  # Replace with your microphone device indexes

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open streams for each microphone
    streams = [
                audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=idx, frames_per_buffer=CHUNK)
                for idx in DEVICE_INDEXES
            ]

    print("Recording...")

    # Record audio
    frames = [[] for _ in DEVICE_INDEXES]
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        for i, stream in enumerate(streams):
            data = stream.read(CHUNK)
            frames[i].append(data)

    print("Finished recording.")

    # Save audio to files
    for i, frame in enumerate(frames):
        wf = wave.open(OUTPUT_FILES[i], 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frame))
        wf.close()

    # Close streams
    for stream in streams:
        stream.stop_stream()
        stream.close()
    audio.terminate()


def recordsound4():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 2
    OUTPUT_FILES = ["channel4.wav"]  # Output files for each microphone
    DEVICE_INDEXES = [3]  # Replace with your microphone device indexes

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open streams for each microphone
    streams = [
                audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=idx, frames_per_buffer=CHUNK)
                for idx in DEVICE_INDEXES
            ]

    print("Recording...")

    # Record audio
    frames = [[] for _ in DEVICE_INDEXES]
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        for i, stream in enumerate(streams):
            data = stream.read(CHUNK)
            frames[i].append(data)

    print("Finished recording.")

    # Save audio to files
    for i, frame in enumerate(frames):
        wf = wave.open(OUTPUT_FILES[i], 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frame))
        wf.close()

    # Close streams
    for stream in streams:
        stream.stop_stream()
        stream.close()
    audio.terminate()


if __name__ == "__main__":

    channel_list=[1,2,3]
    positionTable={1:[1,2,4],2:[2,3,4]}

    mc = MyCobot280("COM3", 115200)
    if mc.get_fresh_mode() != 1:
        mc.set_fresh_mode(1)
    
    #posicion inicial
    mc.send_angles([0,0,0,0,0,0], 3)

    wait4location(20)

    #Obtener ubicacion
    angles=mc.get_angles()
    print(angles)
    coords=mc.get_coords()
    getlocation(coords)

    print("Press any key to continue...")
    msvcrt.getch()

    #round1 step 10 degrees
    #1) swap axis 6     0->90  10 points
    #2) swap axis 2   10->130  13 points
    #3) swap axis 1 -160->160  32 points
    
    # Get the current time
    start_time = datetime.now().time()

    for axis1 in range(-140,-130,10):
        mc.send_angle(1,axis1,5)
        wait4location(10)
        coords=mc.get_coords()
        getlocation(coords)
        for axis2 in range(10,140,10):
            mc.send_angle(2,axis2,2)
            wait4location(12)
            for axis6 in range(0,90,10):
                mc.send_angle(6,axis6,2)
                wait4location(5)
                coords=mc.get_coords()
                location=getlocation(coords)
            
                ubication="Ubicacion_"+location[0]+"_"+location[1]+"_"+location[2]
                orientation="Orientacion_"+location[3]+"_"+location[4]+"_"+location[5]

                position= ubication+"_"+orientation

                #set robot2position
                #wait
                os.makedirs("Position__"+position, exist_ok=True)
                root = os.getcwd()
                os.chdir("Position__"+position)

                #channel1
                process1 = Process(target=recordsound1)
                process2 = Process(target=soundtrigger)

                process1.start()
                process2.start()

                process1.join()
                process2.join()

                time.sleep(4)

                #channel2
                process1 = Process(target=recordsound2)
                process2 = Process(target=soundtrigger)

                process1.start()
                process2.start()

                process1.join()
                process2.join()

                time.sleep(4)

                #channel3
                process1 = Process(target=recordsound3)
                process2 = Process(target=soundtrigger)

                process1.start()
                process2.start()

                process1.join()
                process2.join()


                time.sleep(4)

                #channel4
                process1 = Process(target=recordsound4)
                process2 = Process(target=soundtrigger)

                process1.start()
                process2.start()

                process1.join()
                process2.join()

                time.sleep(4)

                os.chdir(root)

    #Posicion de descanso
    wait4location(20)
    mc.send_angles([-2.28, -91.14, -74.17, 83.49, 0.35, -117.68], 3)
    end_time = datetime.now().time()
    print("Start_time="+str(start_time))
    print("End_time="+str(end_time))