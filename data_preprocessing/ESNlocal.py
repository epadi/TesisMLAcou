import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap
import math
from operator import itemgetter
import torch
from torch import nn
from torch.utils.data import Dataset
from torch.utils.data import DataLoader, random_split
import torch.optim as optim
import torchvision
from torchvision.io import decode_image
import torchvision.transforms as transforms
from tqdm import tqdm
import skimage
from skimage import data, feature,io
from PIL import Image
from random import shuffle
import cv2
import statistics
import torchaudio
import soundfile as sf


def load_audio_tensor(path, target_length=20000):
    waveform, sample_rate = sf.read(path, always_2d=False, dtype='float32')

    if waveform.ndim == 1:
        waveform = waveform[None, :]
    else:
        waveform = waveform.T

    if waveform.shape[1] < target_length:
        pad = target_length - waveform.shape[1]
        waveform = np.pad(waveform, ((0, 0), (0, pad)), mode='constant')
    else:
        waveform = waveform[:, :target_length]

    return torch.tensor(waveform, dtype=torch.float32), sample_rate


imagesnames=os.listdir('C:/Users/Esteban/TesisCode/Recordings/WW27_Rec/Datasets/audioch1_dataset')

with open('C:/Users/Esteban/TesisCode/Recordings/WW27_Rec/Datasets/audioch1.csv', 'w') as file:
  for name in imagesnames:
    namesbytokens=name.split("_")[0]
    labeltoken= str(int(re.sub(r'[^0-9]', '',namesbytokens))-1)
    file.write(name+","+labeltoken+"\n")   #namesbytokens[0] = Session#


class AudioDataset(Dataset):
    def __init__(self, csv_file, audio_dir, transform=None):
        self.annotations = pd.read_csv(csv_file, header=None, names=['filename', 'label'])
        self.audio_dir = audio_dir
        self.transform = transform

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, index):
        audio_path = os.path.join(self.audio_dir, self.annotations.iloc[index, 0])
        waveform, sample_rate = load_audio_tensor(audio_path)
        label = self.annotations.iloc[index, 1]

        if self.transform:
            waveform = self.transform(waveform)

        return waveform, label

# Define paths
CSV_FILE = 'C:/Users/Esteban/TesisCode/Recordings/WW27_Rec/Datasets/audioch1.csv'
AUDIO_DIR = 'C:/Users/Esteban/TesisCode/Recordings/WW27_Rec/Datasets/audioch1_dataset'

# Create the dataset
dataset = AudioDataset(csv_file=CSV_FILE, audio_dir=AUDIO_DIR)

# Get a sample to determine expected input shape (assuming all audio files have similar characteristics after loading)
# waveform, label = dataset[0]
# print(f"Sample Waveform Shape: {waveform.shape}")
# print(f"Sample Label: {label}")

# Define split ratios
train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size

# Split the dataset
train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

# Create DataLoaders
BATCH_SIZE = 32 # You can adjust this batch size

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

print(f"Number of training samples: {len(train_dataset)}")
print(f"Number of testing samples: {len(test_dataset)}")
print(f"Number of training batches: {len(train_loader)}")
print(f"Number of testing batches: {len(test_loader)}")

# You can iterate through a DataLoader to get batches:
# for waveforms, labels in train_loader:
#    print(f"Batch waveforms shape: {waveforms.shape}")
#    print(f"Batch labels shape: {labels.shape}")
#    brea

import torchaudio.transforms as T

# Get a sample rate from the first audio file to configure MFCCs
# This assumes all audio files have the same sample rate
sample_waveform, sample_rate = load_audio_tensor(os.path.join(AUDIO_DIR, dataset.annotations.iloc[0, 0]))
print(f"Detected Sample Rate: {sample_rate} Hz")

# Define MFCC transform
# n_mfcc: Number of MFCCs to retain
# melkwargs: Parameters for the MelSpectrogram, including n_fft and hop_length
# The number of frames (time steps) will vary, so we'll need padding
# Using 40 MFCCs as a common value
mfcc_transform = T.MFCC(
    sample_rate=sample_rate,
    n_mfcc=40,
    melkwargs={
        "n_fft": 400,
        "hop_length": 160,
        "n_mels": 64
    }
)

# Update the dataset with the transform
dataset.transform = mfcc_transform

# Redefine the AudioDataset class to handle multiple channels if needed and ensure correct MFCC input
class AudioDataset(Dataset):
    def __init__(self, csv_file, audio_dir, transform=None):
        self.annotations = pd.read_csv(csv_file, header=None, names=['filename', 'label'])
        self.audio_dir = audio_dir
        self.transform = transform

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, index):
        audio_path = os.path.join(self.audio_dir, self.annotations.iloc[index, 0])
        waveform, sample_rate = load_audio_tensor(audio_path)

        # Ensure mono audio if multiple channels are present, or handle accordingly
        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True) # Convert to mono by averaging channels

        if self.transform:
            # MFCC transform expects (channels, samples) and outputs (channels, n_mfcc, time_steps)
            features = self.transform(waveform) # Output will be (1, n_mfcc, time_steps)
            features = features.squeeze(0) # Squeeze the channel dimension to (n_mfcc, time_steps)
        else:
            features = waveform # If no transform, return raw waveform (channel, samples)

        label = self.annotations.iloc[index, 1]

        return features, label


# Instantiate the dataset again with the MFCC transform
dataset = AudioDataset(csv_file=CSV_FILE, audio_dir=AUDIO_DIR, transform=mfcc_transform)

# Redefine DataLoaders with the updated dataset
train_dataset, test_dataset = random_split(dataset, [train_size, test_size])


# Custom collate_fn for padding MFCC sequences
def collate_fn(batch):
    # batch is a list of (features, label) tuples
    features, labels = zip(*batch)

    # features will be a list of tensors with shape (n_mfcc, time_steps)
    # Find the maximum time_steps in the current batch
    max_len = max([f.shape[1] for f in features])

    # Pad each feature tensor to max_len
    padded_features = []
    for f in features:
        # Pad with zeros at the end along the time_steps dimension
        padding_needed = max_len - f.shape[1]
        padded_f = torch.nn.functional.pad(f, (0, padding_needed)) # (left_pad, right_pad) for last dimension
        padded_features.append(padded_f)

    # Stack the padded features and labels
    padded_features = torch.stack(padded_features)
    labels = torch.tensor(labels, dtype=torch.long)

    return padded_features, labels


# Create DataLoaders with custom collate_fn
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate_fn)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False, collate_fn=collate_fn)

print(f"Number of training samples: {len(train_dataset)}")
print(f"Number of testing samples: {len(test_dataset)}")
print(f"Number of training batches (with MFCCs & collate_fn): {len(train_loader)}")
print(f"Number of testing batches (with MFCCs & collate_fn): {len(test_loader)}")

# Verify the output shape of a batch
for mfcc_features, labels in train_loader:
    print(f"MFCC Features Batch Shape: {mfcc_features.shape}") # (batch_size, n_mfcc, max_time_steps)
    print(f"Labels Batch Shape: {labels.shape}") # (batch_size)
    break

class ESNLayer(nn.Module):
    def __init__(self, input_size, reservoir_size, spectral_radius=0.9, sparsity=0.5):
        super(ESNLayer, self).__init__()

        self.input_size = input_size
        self.reservoir_size = reservoir_size
        self.spectral_radius = spectral_radius
        self.sparsity = sparsity

        self.W_in = nn.Linear(input_size, reservoir_size, bias=False)
        nn.init.kaiming_uniform_(self.W_in.weight)
        self.W_in.weight.requires_grad = False

        self.W_res = nn.Linear(reservoir_size, reservoir_size, bias=False)
        self._initialize_reservoir_weights()
        self.W_res.weight.requires_grad = False

    def _initialize_reservoir_weights(self):
        nn.init.uniform_(self.W_res.weight, -1.0, 1.0)
        mask = (torch.rand(self.reservoir_size, self.reservoir_size) > self.sparsity).float()
        self.W_res.weight.data = self.W_res.weight.data * mask

        with torch.no_grad():
            eigvals = torch.linalg.eigvals(self.W_res.weight.data).abs()
            current_spectral_radius = torch.max(eigvals).item()
            if current_spectral_radius > 0:
                self.W_res.weight.data = self.W_res.weight.data * (self.spectral_radius / current_spectral_radius)

    def forward(self, input_sequence):
        # input_sequence shape: (batch_size, input_dim, time_steps)
        batch_size, _, time_steps = input_sequence.shape
        batch_reservoir_states = torch.zeros(batch_size, self.reservoir_size, device=input_sequence.device)

        for t in range(time_steps):
            u_t = input_sequence[:, :, t]
            batch_reservoir_states = torch.tanh(
                self.W_in(u_t) + self.W_res(batch_reservoir_states)
            )

        return batch_reservoir_states


class DeepEchoStateNetwork(nn.Module):
    def __init__(self, input_size, reservoir_size, output_size, num_layers=4, spectral_radius=0.9, sparsity=0.5):
        super(DeepEchoStateNetwork, self).__init__()

        self.num_layers = num_layers
        self.reservoir_size = reservoir_size
        self.esn_layers = nn.ModuleList([
            ESNLayer(input_size if i == 0 else reservoir_size, reservoir_size, spectral_radius, sparsity)
            for i in range(num_layers)
        ])
        self.W_out = nn.Linear(reservoir_size, output_size)

    def forward(self, input_sequence):
        # Use the final hidden state of each ESN as the input to the next layer
        current_state = input_sequence

        for layer in self.esn_layers:
            current_state = layer(current_state)
            current_state = current_state.unsqueeze(-1)

        return self.W_out(current_state.squeeze(-1))

# Determine input_size and output_size
# input_size is the number of MFCCs
input_size = mfcc_transform.n_mfcc

# output_size is the number of unique labels (sessions)
output_size = dataset.annotations['label'].nunique()

# DESN hyperparameters
RESERVOIR_SIZE = 1000 # A common starting point, can be tuned
NUM_ESN_LAYERS = 4
SPECTRAL_RADIUS = 0.99 # Should be < 1 for stability
SPARSITY = 0.2 # Proportion of zero connections

# Instantiate the DESN model
model = DeepEchoStateNetwork(
    input_size=input_size,
    reservoir_size=RESERVOIR_SIZE,
    output_size=output_size,
    num_layers=NUM_ESN_LAYERS,
    spectral_radius=SPECTRAL_RADIUS,
    sparsity=SPARSITY
)

print(f"DESN Model:\n{model}")
print(f"Input Size: {input_size}")
print(f"Output Size (Number of Classes): {output_size}")
print(f"Reservoir Size: {RESERVOIR_SIZE}")
print(f"Number of ESN Layers: {NUM_ESN_LAYERS}")

# Check if CUDA is available and move model to GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
print(f"Model moved to: {device}")

# Define Loss Function and Optimizer
criterion = nn.CrossEntropyLoss()

# For DESN, we only train the output layer (W_out)
optimizer = optim.Adam(model.W_out.parameters(), lr=0.001)

def train_epoch(model, train_loader, criterion, optimizer, device):
    model.train() # Set model to training mode
    running_loss = 0.0
    correct_predictions = 0
    total_samples = 0

    for mfcc_features, labels in tqdm(train_loader, desc="Training"):
        mfcc_features, labels = mfcc_features.to(device), labels.to(device)

        optimizer.zero_grad()

        # Forward pass
        outputs = model(mfcc_features)
        loss = criterion(outputs, labels)

        # Backward pass and optimize
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * mfcc_features.size(0)
        _, predicted = torch.max(outputs.data, 1)
        total_samples += labels.size(0)
        correct_predictions += (predicted == labels).sum().item()

    epoch_loss = running_loss / total_samples
    epoch_accuracy = correct_predictions / total_samples
    return epoch_loss, epoch_accuracy

def evaluate_model(model, test_loader, criterion, device):
    model.eval() # Set model to evaluation mode
    running_loss = 0.0
    correct_predictions = 0
    total_samples = 0

    with torch.no_grad(): # Disable gradient calculation for evaluation
        for mfcc_features, labels in tqdm(test_loader, desc="Evaluating"):
            mfcc_features, labels = mfcc_features.to(device), labels.to(device)

            outputs = model(mfcc_features)
            loss = criterion(outputs, labels)

            running_loss += loss.item() * mfcc_features.size(0)
            _, predicted = torch.max(outputs.data, 1)
            total_samples += labels.size(0)
            correct_predictions += (predicted == labels).sum().item()

    epoch_loss = running_loss / total_samples
    epoch_accuracy = correct_predictions / total_samples
    return epoch_loss, epoch_accuracy

NUM_EPOCHS = 100 # You can adjust the number of epochs

train_losses = []
train_accuracies = []

print("Starting training...")
for epoch in range(NUM_EPOCHS):
    train_loss, train_accuracy = train_epoch(model, train_loader, criterion, optimizer, device)

    train_losses.append(train_loss)
    train_accuracies.append(train_accuracy)

    print(f"Epoch {epoch+1}/{NUM_EPOCHS}:\n" \
          f"Train Loss: {train_loss:.4f}, Train Accuracy: {train_accuracy:.4f}")

print("Training finished!\n")

# Perform evaluation only at the end of training
print("Starting final evaluation...")
final_test_loss, final_test_accuracy = evaluate_model(model, test_loader, criterion, device)
print(f"Final Test Loss: {final_test_loss:.4f}, Final Test Accuracy: {final_test_accuracy:.4f}")


# Plotting results
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(train_losses, label='Train Loss')
plt.title('Training Loss over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(train_accuracies, label='Train Accuracy')
plt.title('Training Accuracy over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()