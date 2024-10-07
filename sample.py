import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "2"
import torch

if torch.cuda.is_available():
        device = torch.device('cuda')

print(device)

import librosa

y,sr = librosa.load('/workspace/dataset/tess_datasets/train/train_data/OAF_back_happy.wav', sr=16000)

print(y.shape)
print(sr)