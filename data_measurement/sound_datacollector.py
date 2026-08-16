import pyaudio
import os
import time
import msvcrt
from playsound import playsound
from multiprocessing import Process
import wave
from pathlib import Path
import shutil
#from pymycobot.mycobot280 import MyCobot280
from datetime import datetime
import serial
import argparse
import threading



def read_serial():
    global rdata
    while True:
        data = ser.readline().decode('utf-8')
        if data:
            print(f"Received: {data}", end='')
            rdata=data

def writeanglocation(base,shoulder,elbow,hand,speed,acceleration):
    command = "{\"T\":122"
    command = command + ",\"b\":" + str(base)
    command = command + ",\"s\":" + str(shoulder)
    command = command + ",\"e\":" + str(elbow)
    command = command + ",\"h\":" + str(hand)
    command = command + ",\"spd\":" + str(speed)
    command = command + ",\"acc\":" + str(acceleration) + "}"
    #command = "{\"T\":122,\"b\":0,\"s\":0,\"e\":0,\"h\":180,\"spd\":30,\"acc\":3}"
    ser.write(command.encode() + b'\n')

def writesingleang(joint,angle,speed,acceleration):
    command = "{\"T\":121"
    command = command + ",\"joint\":" + str(joint)
    command = command + ",\"angle\":" + str(angle)
    command = command + ",\"spd\":" + str(speed)
    command = command + ",\"acc\":" + str(acceleration) + "}"
    #command = "{"T":121,"joint":1,"angle":0,"spd":10,"acc":10}"
    ser.write(command.encode() + b'\n')

def writecoordlocation(xcoord,ycoord,zcoord,trot,speed):
    command = "{\"T\":104"
    command = command + ",\"x\":" + str(xcoord)
    command = command + ",\"y\":" + str(ycoord)
    command = command + ",\"z\":" + str(zcoord)
    command = command + ",\"t\":" + str(trot)
    command = command + ",\"spd\":" + str(speed) + "}"
    #command = {"T":104,"x":235,"y":0,"z":234,"t":3.14,"spd":0.25}
    ser.write(command.encode() + b'\n')


def readlocation():
    command = "{\"T\":105}"
    ser.write(command.encode() + b'\n')
    #readresponse
    retdata=""
    while True:
        data = ser.readline().decode('utf-8')
        if data:
            if data.find("\"T\":1051") != -1:
                retdata=data
                break
    return retdata

def getlocation(stringlocation):
   splitstring=stringlocation.split(",")
   xcord=splitstring[1].split(":")[1]
   ycord=splitstring[2].split(":")[1]
   zcord=splitstring[3].split(":")[1]
   return [xcord, ycord, zcord]


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
    RECORD_SECONDS = 1
    OUTPUT_FILES = ["channel1.wav"]  # Output files for each microphone
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


def recordsound2():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 1
    OUTPUT_FILES = ["channel2.wav"]  # Output files for each microphone
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


def recordsound3():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 1
    OUTPUT_FILES = ["channel3.wav"]  # Output files for each microphone
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


def recordsound4():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 1
    OUTPUT_FILES = ["channel4.wav"]  # Output files for each microphone
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


rdata=""
if __name__ == "__main__":
    #main()
    global ser
    #serial init
    ser = serial.Serial("COM5", baudrate=115200, dsrdtr=None)
    ser.setRTS(False)
    ser.setDTR(False)

    #turnoff wifi
    command = "{\"T\":401,\"cmd\":0}"
    ser.write(command.encode() + b'\n')
    
    #go to initial position
    writeanglocation(-180,0,45,0,30,3)
    #wait for the movement
    wait4location(20)

    #get the location and log it
    rldata=readlocation()
    location=getlocation(rldata)
    print(location)
    
    print("Press any key to continue...")
    msvcrt.getch()
    
    #movements
    #1) Base -180 --> 180 
    #2) Zaxis topzlocation --> topzlocation-30
    #3) orientation 50-->140 

    #showroom var for debug to only display movement
    showroom=0
    #get the start time
    start_time = datetime.now().time()
    #-180  70  10
    for angbase in [-90]:#range (60,70,10):-95,5,55]
        print(angbase)
        #go to base initial location
        writeanglocation(angbase,0,45,0,30,3)
        #wain until movement complete
        wait4location(10)
        
        #get location
        rldata=readlocation()
        location=getlocation(rldata)
        xlocation=float(location[0])
        ylocation=float(location[1])
        zlocation=float(location[2])

        #Z initial location
        zmov=zlocation
        if showroom==1:
            continue
        #0,30,1
        for steps in range(0,30,1):

            #From the base position keep the angle and only decrease z
            writecoordlocation(xlocation,ylocation,zmov,0,0.2)
            wait4location(10)
            zmov=zmov-20
            if showroom==2:
                continue
            #50, 140, 10
            for anglerot in range (50,140,10):

                
                writesingleang(4,anglerot,30,3)
                wait4location(3)
                #get location
                rldata=readlocation()
                
                location=getlocation(rldata)
                
                ubication="Ubicacion_"+location[0]+"_"+location[1]+"_"+location[2]
                orientation="Orientacion_"+str(anglerot)
                
                position= ubication+"_"+orientation

                #build directory robot2position
                #wait
                os.makedirs("Position__"+position, exist_ok=True)
                root = os.getcwd()
                os.chdir("Position__"+position)

                #dummy
                processdummy = Process(target=soundtrigger)
                processdummy.start()
                processdummy.join()
                time.sleep(1)

                #channel1
                process1 = Process(target=recordsound1)
                process2 = Process(target=soundtrigger)

                process1.start()
                process2.start()

                process1.join()
                process2.join()

                #time.sleep(1)

                #channel2
                process1 = Process(target=recordsound2)
                process2 = Process(target=soundtrigger)

                process1.start()
                process2.start()

                process1.join()
                process2.join()

                #time.sleep(1)

                #channel3
                process1 = Process(target=recordsound3)
                process2 = Process(target=soundtrigger)

                process1.start()
                process2.start()

                process1.join()
                process2.join()

                #time.sleep(1)

                #channel4
                process1 = Process(target=recordsound4)
                process2 = Process(target=soundtrigger)

                process1.start()
                process2.start()

                process1.join()
                process2.join()

                #time.sleep(1)

                os.chdir(root)
        if showroom==2:
            break
    
    #go to final-rest position 
    wait4location(20)
    writeanglocation(0,-30,160,0,30,3)
    end_time = datetime.now().time()
    print("Start_time="+str(start_time))
    print("End_time="+str(end_time))
