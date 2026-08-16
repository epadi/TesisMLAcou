import os
import torch
import torchaudio
import torchaudio.transforms as T
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def get_directories(path='.'):
    return [entry.name for entry in os.scandir(path) if entry.is_dir()]

#channel="aligned_channel2.wav"
signals_path='C:/Users/Esteban/TesisCode/Recordings/WW27_Rec/'
audio_directory="audiobfmXposch3Ch1_dataset"
image_directory="audio2imagebfmXposch3ch1_dataset"

os.chdir(signals_path)
os.makedirs(image_directory, exist_ok=True)
os.chdir(image_directory)

for audiofile in os.listdir(signals_path+"/"+audio_directory):
    audiopath=signals_path+"/"+audio_directory+"/"+audiofile

    print(audiopath)
    if os.path.exists(audiopath):
        #print(audiopath)
        waveform, sample_rate = torchaudio.load(audiopath)
        # Define MelSpectrogram transform
        mel_spectrogram_transform = T.MelSpectrogram(
        sample_rate=sample_rate,
        n_fft=2048,
        hop_length=512,
        n_mels=128
        )

        # Compute Mel Spectrogram
        mel_spectrogram = mel_spectrogram_transform(waveform)

        # Convert to Log scale
        log_mel_spectrogram = torch.log(mel_spectrogram + 1e-9)  # Add small value to avoid log(0)

        # Plot the Log Mel Spectrogram
        plt.figure(figsize=(6, 4))
        plt.imshow(log_mel_spectrogram[0].numpy(), aspect="auto", origin="lower")
        plt.axis('off') 
        plt.tight_layout()
        plt.savefig(signals_path+"/"+image_directory+"/"+audiofile+".jpg",bbox_inches='tight', pad_inches=0)

