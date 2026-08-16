
import pyaudio
import wave

# Initialize PyAudio
audio = pyaudio.PyAudio()

# List all available devices
for i in range(audio.get_device_count()):
    print(f"Device {i}: {audio.get_device_info_by_index(i)['name']}")

# Select device indices for your microphones
mic1_index = 1  # Replace with your first mic's index
mic2_index = 3  # Replace with your second mic's index

# Parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5

# Open streams for both microphones
stream1 = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=mic1_index, frames_per_buffer=CHUNK)
stream2 = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=mic2_index, frames_per_buffer=CHUNK)

print("Recording...")

frames1 = []
frames2 = []

for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data1 = stream1.read(CHUNK)
    data2 = stream2.read(CHUNK)
    frames1.append(data1)
    frames2.append(data2)

print("Finished recording.")

# Stop and close streams
stream1.stop_stream()
stream1.close()
stream2.stop_stream()
stream2.close()
audio.terminate()

# Save recordings
with wave.open("mic1_output.wav", "wb") as wf1:
    wf1.setnchannels(CHANNELS)
    wf1.setsampwidth(audio.get_sample_size(FORMAT))
    wf1.setframerate(RATE)
    wf1.writeframes(b''.join(frames1))

with wave.open("mic2_output.wav", "wb") as wf2:
    wf2.setnchannels(CHANNELS)
    wf2.setsampwidth(audio.get_sample_size(FORMAT))
    wf2.setframerate(RATE)
    wf2.writeframes(b''.join(frames2))




