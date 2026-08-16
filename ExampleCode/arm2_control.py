import serial
import argparse
import threading
import time

rdata=""

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


def main():
    global ser
    global rdata

    ser = serial.Serial("COM7", baudrate=115200, dsrdtr=None)
    ser.setRTS(False)
    ser.setDTR(False)

    #turnoff wifi
    command = "{\"T\":401,\"cmd\":0}"
    ser.write(command.encode() + b'\n')
    
    #goto origin
    writeanglocation(-180,0,45,0,30,3)
    #wait 5 seconds
    time.sleep(10)

    #Move the cube in space with 3 joint movements
    for angbase in range (-180,-100,40):
        #print(angbase)
        writeanglocation(angbase,0,45,0,30,3)
        #wait 5 seconds
        time.sleep(10)
        rldata=readlocation()
        location=getlocation(rldata)
        xlocation=float(location[0])
        ylocation=float(location[1])
        zlocation=float(location[2])

        #movement on Z
        zmov=zlocation
        for steps in range(0,30,1):
            zmov=zmov-20
            writecoordlocation(xlocation,ylocation,zmov,0,0.5)
            time.sleep(1)
            rldata=readlocation()
            location=getlocation(rldata)
            #print(location)
            
            #change orientation
            for angle in range (50,140,10):
                print(angle)
                writesingleang(4,angle,30,3)
                time.sleep(1)

    rldata=readlocation()
    print(rldata)

    #time.sleep(4)
    #ser.close()


if __name__ == "__main__":
    main()