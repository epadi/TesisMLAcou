import os
import torch
import torchaudio
import torchaudio.transforms as T
import matplotlib.pyplot as plt
import shutil

#This script is to create a audio dataset format directory


def get_directories(path='.'):
    return [entry.name for entry in os.scandir(path) if entry.is_dir()]


def copy_file(source_path, destination_path):
    """
    Copies a file from source_path to destination_path.
    Preserves file metadata using shutil.copy2().
    """
    try:
        # Validate that the source file exists
        if not os.path.isfile(source_path):
            raise FileNotFoundError(f"Source file not found: {source_path}")

        # Ensure the destination directory exists
        dest_dir = os.path.dirname(destination_path)
        if dest_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # Copy the file (with metadata)
        shutil.copy2(source_path, destination_path)
        print(f"File copied successfully from '{source_path}' to '{destination_path}'.")

    except PermissionError:
        print("Error: Permission denied. Check your file and folder permissions.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except IsADirectoryError:
        print("Error: Destination path is a directory, not a file.")
    except Exception as e:
        print(f"Unexpected error: {e}")


channel="aligned_channel4.wav"
source_path='C:/Users/Esteban/python_code/Recordings/WW27_Rec/Test_sessions'
dest_path='C:/Users/Esteban/python_code/Recordings/WW27_Rec/Test_sessions'
new_directory="audioch4_dataset"

source_directories=get_directories(source_path)

os.chdir(dest_path)
os.makedirs(new_directory, exist_ok=True)


for directory in source_directories:
    #os.makedirs(directory, exist_ok=True)
    subdirectories=get_directories(source_path+"/"+directory)
    for subdirectory in subdirectories:
        if "Orientacion" in subdirectory:
            audiopath=source_path+"/"+directory+"/"+subdirectory+"/"+channel
            if os.path.exists(audiopath):
                copy_file(audiopath, dest_path+"/"+new_directory+"/"+directory+"_"+subdirectory+"_ch4.wav")
                
