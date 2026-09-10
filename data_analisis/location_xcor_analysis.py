import os
import numpy as np
import math
from audio2numpy import open_audio
from operator import itemgetter
import matplotlib.pyplot as plt
from scipy.signal import correlate
import json

def normalized_cross_correlation(signal1, signal2):
    signal1 = np.asarray(signal1).squeeze()
    signal2 = np.asarray(signal2).squeeze()
    signal1 = signal1 - np.mean(signal1)
    signal2 = signal2 - np.mean(signal2)
    denominator = np.linalg.norm(signal1) * np.linalg.norm(signal2)
    if denominator == 0:
        return 0.0
    return float(np.max(correlate(signal1, signal2, mode='full')) / denominator)


reference_path='C:/Users/Esteban/TesisCode/Recordings/WW27_Rec/S26/'
directory_name='Position__Ubicacion_90.33688561_216.2139435_9.314473701_Orientacion_50'
reference_signal_path=os.path.join(reference_path, directory_name)

channel="aligned_channel1.wav"
samplerate = 44100
dimension = "z"
required_orientation = 50

def get_location_from_directory(dirname):
    parts = os.path.basename(dirname).split('_')
    return {
        "x": float(parts[3]),
        "y": float(parts[4]),
        "z": float(parts[5]),
    }

def get_orientation_from_directory(dirname):
    return float(os.path.basename(dirname).split('_')[7])

reference_location = get_location_from_directory(reference_signal_path)
threshold = reference_location[dimension]
recordings_path = os.path.dirname(reference_signal_path)
candidate_directories = []

for entry in os.scandir(recordings_path):
    if not entry.is_dir():
        continue
    location = get_location_from_directory(entry.name)
    if (
        get_orientation_from_directory(entry.name) == required_orientation
        and location[dimension] < threshold
    ):
        distance = math.sqrt(sum(
            (location[axis] - reference_location[axis]) ** 2
            for axis in ("x", "y", "z")
        ))
        candidate_directories.append((distance, entry.path, location))

signal_same_orientation_paths = [
    path for _, path, _ in sorted(candidate_directories, key=itemgetter(0))[:10]
]
selected_candidates = sorted(candidate_directories, key=itemgetter(0))[:10]

print(f"10 nearest directories with {dimension.upper()} < {threshold}:")
for distance, path, location in sorted(candidate_directories, key=itemgetter(0))[:10]:
    print(f"{path} | distance={distance:.6f} | location={location}")

signal_cross_ordpoints=[]
ref_signal, samplerate = open_audio(reference_signal_path + "/" + channel)
for path in signal_same_orientation_paths:
    signal, samplerate = open_audio(path + "/" + channel)
    signal_cross_ordpoints.append(normalized_cross_correlation(ref_signal, signal))


distances = [distance for distance, _, _ in selected_candidates]
plt.plot(distances, signal_cross_ordpoints, color='purple', linestyle='--', marker='s', linewidth=2, markersize=8)
plt.title("normalized cross correlation vs Euclidean distance")
plt.xlabel("Euclidean distance from reference location")
plt.ylabel("normalized cross-correlation coefficient")
plt.show()



