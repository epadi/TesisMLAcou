import os
import shutil

def get_directories(path='.'):
    return [entry.name for entry in os.scandir(path) if entry.is_dir()]


def copy_file(src_path, dest_path):
    """
    Copy a file from src_path to dest_path.
    If dest_path is a directory, the file will be copied inside it.
    """
    try:
        # Validate that the source file exists
        if not os.path.isfile(src_path):
            print(f"Error: Source file '{src_path}' does not exist.")
            return

        # If destination is a directory, keep the same filename
        if os.path.isdir(dest_path):
            dest_path = os.path.join(dest_path, os.path.basename(src_path))

        # Ensure the destination directory exists
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        # Copy the file (preserves metadata like modification time)
        shutil.copy2(src_path, dest_path)
        print(f"File copied successfully to: {dest_path}")

    except PermissionError:
        print("Error: Permission denied. Check your file and folder permissions.")
    except Exception as e:
        print(f"Unexpected error: {e}")


signals_path='C:/Users/Esteban/python_code/Recordings/WW27_Rec/Datasets/'

sourceimage_directory="audio2imagech4_dataset"
destimage_directory="audio2imagech4_onlyloc_dataset"

os.chdir(signals_path)
os.makedirs(destimage_directory, exist_ok=True)
os.chdir(destimage_directory)

for imagename in os.listdir(signals_path+"/"+sourceimage_directory):

    if "Orientacion_60" in imagename:
        print(imagename)
        source_file = signals_path+"/"+sourceimage_directory+"/"+imagename
        destination = signals_path+"/"+destimage_directory
        copy_file(source_file, destination)
