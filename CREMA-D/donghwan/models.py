import torch
import torch.nn as nn

class CNN(nn.Module):
    def __init__(self, in_channels):
        super().__init__()

        self.cnn = nn.Sequential(
            nn.Conv1d(in_channels=in_channels, out_channels=64, kernel_size=3, padding=1),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Conv1d(in_channels=64, out_channels=128, kernel_size=3, padding=1),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, padding=1),
            nn.AdaptiveAvgPool1d(output_size=1)
        )
        self.fc1 = nn.Linear(128, 1)

    def forward(self, x):
        x = x.permute(0, 2, 1)  # [batch_size, sequence_length, features]
        x = self.cnn(x)
        x = x.squeeze()
        emotion = self.fc1(x)
        return emotion

class ResNetCNN(nn.Module):
    def __init__(self, in_channels):
        super(ResNetCNN, self).__init__()

        # 첫 번째 Conv 층
        self.initial_conv = nn.Sequential(
            nn.Conv1d(in_channels=in_channels, out_channels=64, kernel_size=3, padding=1),
            nn.BatchNorm1d(64),
            nn.ReLU()
        )
        
        # Residual Blocks
        self.res_block1 = ResidualBlock(in_channels=64, out_channels=64)
        self.res_block2 = ResidualBlock(in_channels=64, out_channels=128)
        self.res_block3 = ResidualBlock(in_channels=128, out_channels=128)
        
        # Adaptive Average Pooling 및 Fully Connected Layer
        self.pool = nn.AdaptiveAvgPool1d(output_size=1)
        self.fc1 = nn.Linear(128, 1)

    def forward(self, x):
        x = x.permute(0, 2, 1)  # [batch_size, features, sequence_length]

        # Initial Conv
        x = self.initial_conv(x)
        
        # Residual Blocks
        x = self.res_block1(x)
        x = self.res_block2(x)
        x = self.res_block3(x)
        
        # Adaptive Average Pooling
        x = self.pool(x)
        x = x.squeeze(dim=-1)  # [batch_size, 128]

        # Fully Connected Layer
        emotion = self.fc1(x)

        return emotion

class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=3, stride=1, padding=1):
        super(ResidualBlock, self).__init__()
        
        self.conv1 = nn.Conv1d(in_channels, out_channels, kernel_size, stride, padding)
        self.bn1 = nn.BatchNorm1d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv1d(out_channels, out_channels, kernel_size, stride, padding)
        self.bn2 = nn.BatchNorm1d(out_channels)
        
        # 잔차 연결을 위해 입력과 출력의 차원이 맞지 않을 경우 차원 맞추기 위한 Conv1d 층
        self.adjust_channels = nn.Conv1d(in_channels, out_channels, kernel_size=1, stride=stride) if in_channels != out_channels else None

    def forward(self, x):
        identity = x  # 입력 값을 그대로 저장
        
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        
        out = self.conv2(out)
        out = self.bn2(out)
        
        # 잔차 연결: 입력과 현재 층의 출력 값을 더함
        if self.adjust_channels:
            identity = self.adjust_channels(identity)
        
        out += identity
        out = self.relu(out)
        
        return out

class VGG_CNN(nn.Module):
    def __init__(self, in_channels):
        super(VGG_CNN, self).__init__()

        # VGG 스타일의 CNN 아키텍처 정의
        self.features = nn.Sequential(
            # Block 1
            nn.Conv1d(in_channels=in_channels, out_channels=64, kernel_size=3, padding=1),
            nn.BatchNorm1d(64),
            nn.ReLU(inplace=True),
            nn.Conv1d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm1d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool1d(kernel_size=2, stride=2),
            
            # Block 2
            nn.Conv1d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm1d(128),
            nn.ReLU(inplace=True),
            nn.Conv1d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm1d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool1d(kernel_size=2, stride=2),

            # Block 3
            nn.Conv1d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm1d(256),
            nn.ReLU(inplace=True),
            nn.Conv1d(256, 256, kernel_size=3, padding=1),
            nn.BatchNorm1d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool1d(kernel_size=2, stride=2),
        )

        # Fully Connected Layer
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool1d(output_size=1),
            nn.Flatten(),
            nn.Linear(256, 1)
        )

    def forward(self, x):
        x = x.permute(0, 2, 1)  # [batch_size, features, sequence_length]

        x = self.features(x)
        emotion = self.classifier(x)
        
        return emotion

# 테스트용 코드
if __name__ == "__main__":
    # 테스트 시에 feature_type에 따라 모델 초기화
    feature_type = 'mel'  # 예: 'mfcc' 또는 'mel'
    in_channels = 20 if feature_type == 'mfcc' else 128

    model = VGG_CNN(in_channels=in_channels)
    x = torch.randn(16, 126, in_channels)  # [batch_size, sequence_length, features]
    output = model(x)
    print(output.shape)  # [batch_size, 1]
