import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
import os
import torch
import torchaudio
import torchaudio.transforms as T
import matplotlib.pyplot as plt
import shutil



def get_directories(path='.'):
    return [entry.name for entry in os.scandir(path) if entry.is_dir()]

#Audio recordings path
signals_path='C:/Users/Esteban/TesisCode/Recordings/WW27_Rec'
chA="aligned_channel3.wav"
chB="aligned_channel1.wav"
beamformingdir="audiobfmXposch3Ch1_dataset"
time_shift = 0.00125  # seconds


os.chdir(signals_path)
os.makedirs(beamformingdir, exist_ok=True)
os.chdir(beamformingdir)

#directories=get_directories(signals_path)
directories=["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18", "S19", "S20", "S21", "S22", "S23", "S24", "S25", "S26"]

for directory in directories:
    subdirectories=get_directories(signals_path+"/"+directory)
    for subdirectory in subdirectories:
        audio_directory=signals_path+"/"+directory+"/"+subdirectory

        # 1. Read the WAV files
        sample_rate1, data1 = wavfile.read(audio_directory + '/' + chA)
        sample_rate2, data2 = wavfile.read(audio_directory + '/' + chB)

        # 2. Create time axes for both files based on their sample rates
        time1 = np.linspace(0, len(data1) / sample_rate1, num=len(data1))
        time2 = np.linspace(0, len(data2) / sample_rate2, num=len(data2))

        samples_to_shift = int(time_shift * sample_rate2)
        data2 = np.concatenate([np.zeros(samples_to_shift), data2[:-samples_to_shift]])

        # Ensure both signals have the same length for combination
        min_length = min(len(data1), len(data2))
        data1 = data1[:min_length]
        data2 = data2[:min_length]

        # Update time axes to match the new length
        time1 = np.linspace(0, min_length / sample_rate1, num=min_length)
        time2 = np.linspace(0, min_length / sample_rate2, num=min_length)

        # 4. Create combined signal (signal1 + signal2)
        data_combined = data1 + data2
        path_to_save=signals_path+"/"+beamformingdir+"/"+directory+"_"+subdirectory+"_"+"beamformed_ch3_ch1.wav"
        wavfile.write(path_to_save, sample_rate1, data_combined)