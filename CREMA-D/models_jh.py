import torch
import torch.nn as nn

class CNN(nn.Module):
    def __init__(self):
        super().__init__()

        self.cnn = nn.Sequential(
            nn.Conv1d(in_channels=20, out_channels=64, kernel_size=3, padding=1),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Conv1d(in_channels=64, out_channels=128, kernel_size=3, padding=1),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, padding=1),
            nn.AdaptiveAvgPool1d(output_size=1)
        )
        self.fc1 = nn.Linear(128, 1)
        #self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = x.permute(0, 2, 1)  # [배치 크기, 16, 126]
        x = self.cnn(x)
        x = x.squeeze()
        emotion = self.fc1(x)
        #emotion = self.sigmoid(emotion)
        return emotion