import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sys
import os

def spectral_analysis(file_path):
    """
    Perform spectral analysis on a WAV audio file.
    Displays the frequency spectrum in Hz vs amplitude (dB).
    """
    try:
        # Validate file existence
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Read WAV file
        sample_rate, data = wavfile.read(file_path)

        # Ensure mono audio (if stereo, take one channel)
        if data.ndim > 1:
            data = data[:, 0]

        # Normalize audio to range [-1, 1]
        data = data / np.max(np.abs(data))

        # Perform FFT
        N = len(data)
        fft_result = np.fft.fft(data)
        freqs = np.fft.fftfreq(N, 1 / sample_rate)

        # Take only the positive half of the spectrum
        positive_freqs = freqs[:N // 2]
        magnitude = np.abs(fft_result[:N // 2])

        # Convert magnitude to decibels
        magnitude_db = 20 * np.log10(magnitude + 1e-10)  # Avoid log(0)

        # Plot spectrum
        plt.figure(figsize=(10, 6))
        plt.plot(positive_freqs, magnitude_db, color='blue')
        plt.title("Spectral Analysis of Audio Signal")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Magnitude (dB)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except ValueError:
        print("Error: Unsupported audio format. Please use a valid WAV file.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    # Example usage: python script.py audio.wav
    #if len(sys.argv) != 2:
    #    print("Usage: python script.py <audio_file.wav>")
    #    sys.exit(1)

    spectral_analysis("C:/Users/Esteban/python_code/sound3.wav")