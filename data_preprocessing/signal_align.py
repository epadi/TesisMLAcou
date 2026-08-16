import os
import numpy as np
from audio2numpy import open_audio
import soundfile as sf

def get_directories(path='.'):
    return [entry.name for entry in os.scandir(path) if entry.is_dir()]


#This script align the measured signals
#The directory must be at recording session level

signals_path='C:/Users/Esteban/python_code/Recordings/WW27_Rec/Test_sessions/S0.4'

samplerate = 44100
#moverse al directorio
os.chdir(signals_path)
#obtener los directorios de las senales
directories = get_directories(signals_path)

#iterar por los directorios
for directory in directories:
    if directory.find("Position")==0:
        print("Aligning signals for directory: " + directory)
        os.chdir(directory) #Moverse al directorio
        
        #abrir los archivos de audio en np

        #obtenemos el punto de alineacion del canal 1
        if os.path.exists("channel1.wav"):
            array_chanel1, sample_rate1 = open_audio("channel1.wav")
            for index in range(0,array_chanel1.size):
                if array_chanel1[index]>=0.1:
                    align_index_ch1=index
                    break
            ch1_aligned=array_chanel1[(align_index_ch1-1000):(44000+align_index_ch1)]
            sf.write("aligned_channel1.wav",ch1_aligned, samplerate)


        #obtenemos el punto de alineacion del canal 2
        if os.path.exists("channel2.wav"):
            array_chanel2, sample_rate2 = open_audio("channel2.wav")
            for index in range(0,array_chanel2.size):
                if array_chanel2[index]>=0.1:
                    align_index_ch2=index
                    break
            ch2_aligned=array_chanel2[(align_index_ch2-1000):(44000+align_index_ch2)]
            sf.write("aligned_channel2.wav",ch2_aligned, samplerate)


        #obtenemos el punto de alineacion del canal 3
        if os.path.exists("channel3.wav"):
            array_chanel3, sample_rate3 = open_audio("channel3.wav")
            for index in range(0,array_chanel3.size):
                if array_chanel3[index]>=0.1:
                    align_index_ch3=index
                    break
            ch3_aligned=array_chanel3[(align_index_ch3-1000):(44000+align_index_ch3)]
            sf.write("aligned_channel3.wav",ch3_aligned, samplerate)


        #obtenemos el punto de alineacion del canal 4
        if os.path.exists("channel4.wav"):
            array_chanel4, sample_rate4 = open_audio("channel4.wav")
            for index in range(0,array_chanel4.size):
                if array_chanel4[index]>=0.1:
                    align_index_ch4=index
                    break
            ch4_aligned=array_chanel4[(align_index_ch4-1000):(44000+align_index_ch4)]
            sf.write("aligned_channel4.wav",ch4_aligned, samplerate)


        print("los valores de alineacion son: "+str(align_index_ch1)+","+str(align_index_ch2)+","+str(align_index_ch3)+","+str(align_index_ch4))
        
        os.chdir(signals_path)


        