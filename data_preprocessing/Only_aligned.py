import os
import shutil


def get_directories(path='.'):
    return [entry.name for entry in os.scandir(path) if entry.is_dir()]


signals_path='C:/Users/Esteban/python_code/sample'
new_directory="audio_dataset"
os.chdir(signals_path)

directories=get_directories(signals_path)
os.makedirs(new_directory, exist_ok=True)
#directories=["Session1","Session3","Session5"]
os.chdir(new_directory)

for directory in directories:
    os.mkdir(directory)
    subdirectories=get_directories(signals_path+"/"+directory)
    for subdirectory in subdirectories:
        os.mkdir(directory+"/"+subdirectory)
        audiopath2=signals_path+"/"+directory+"/"+subdirectory+"/aligned_channel2.wav"
        shutil.copy2(audiopath2, directory+"/"+subdirectory)
        audiopath3=signals_path+"/"+directory+"/"+subdirectory+"/aligned_channel3.wav"
        shutil.copy2(audiopath3, directory+"/"+subdirectory)
        audiopath4=signals_path+"/"+directory+"/"+subdirectory+"/aligned_channel4.wav"
        shutil.copy2(audiopath4, directory+"/"+subdirectory)



