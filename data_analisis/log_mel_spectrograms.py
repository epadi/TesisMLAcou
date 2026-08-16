import torch
import torchaudio
import torchaudio.transforms as T
import matplotlib.pyplot as plt

# Load audio file
waveform, sample_rate = torchaudio.load("Recordings/New_ARM/Session3/Position__Ubicacion_-216.565074_-72.28111054_-74.27714244_Orientacion_50/aligned_channel2.wav")

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
#plt.imshow(log_mel_spectrogram[0].numpy(), aspect="auto", origin="lower", cmap="viridis")
plt.imshow(log_mel_spectrogram[0].numpy(), aspect="auto", origin="lower")
#plt.title("Log Mel Spectrogram")
plt.axis('off') 
plt.tight_layout()

plt.savefig('Log Mel Spectrogram',bbox_inches='tight', pad_inches=0)
plt.show()