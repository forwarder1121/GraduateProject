import torch
import torch.nn as nn

## note ##
"""
자유 발화 데이터 셋은 차원수가 2개 이므로, 이를 모델이 입력받을 수 있게 조정해야함.
지금은 CNN만 조정 완료
"""

# # CNN 모델 클래스 정의 (이진 분류)
# class CNN(nn.Module):
#     def __init__(self):
#         super(CNN, self).__init__()

#         # 두 개의 채널을 독립적으로 처리하는 두 개의 CNN 모듈
#         self.cnn_left = nn.Sequential(
#             nn.Conv1d(in_channels=16, out_channels=64, kernel_size=3, padding=1),
#             nn.BatchNorm1d(64),
#             nn.ReLU(),
#             nn.Conv1d(in_channels=64, out_channels=128, kernel_size=3, padding=1),
#             nn.BatchNorm1d(128),
#             nn.ReLU(),
#             nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, padding=1),
#             nn.AdaptiveAvgPool1d(output_size=1)
#         )

#         self.cnn_right = nn.Sequential(
#             nn.Conv1d(in_channels=16, out_channels=64, kernel_size=3, padding=1),
#             nn.BatchNorm1d(64),
#             nn.ReLU(),
#             nn.Conv1d(in_channels=64, out_channels=128, kernel_size=3, padding=1),
#             nn.BatchNorm1d(128),
#             nn.ReLU(),
#             nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, padding=1),
#             nn.AdaptiveAvgPool1d(output_size=1)
#         )

#         # 두 채널의 출력을 합친 후 fully connected layer를 적용하여 이진 분류
#         self.fc = nn.Linear(128 * 2, 1)
#         self.sigmoid = nn.Sigmoid()

#     def forward(self, x):
#         # 입력 데이터를 두 개의 채널로 분리
#         left_channel = x[:, 0, :, :]  # 첫 번째 채널
#         right_channel = x[:, 1, :, :]  # 두 번째 채널

#         # 각각의 채널을 독립적으로 처리
#         left_features = self.cnn_left(left_channel)
#         right_features = self.cnn_right(right_channel)

#         # 두 채널의 출력을 합침
#         combined_features = torch.cat((left_features, right_features), dim=1)

#         # 차원을 줄이고 fully connected layer에 입력
#         combined_features = combined_features.squeeze()
#         output = self.fc(combined_features)

#         # 최종 출력 (Sigmoid를 통해 이진 분류 확률 값)
#         output = self.sigmoid(output)
#         return output

class CNN(nn.Module):
    def __init__(self):
        super().__init__()

        self.cnn = nn.Sequential(
            nn.Conv1d(in_channels=16, out_channels=64, kernel_size=3, padding=1),  # 첫 번째 Conv 층
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Conv1d(in_channels=64, out_channels=128, kernel_size=3, padding=1),  # 두 번째 Conv 층
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Conv1d(in_channels=128, out_channels=256, kernel_size=3, padding=1),  # 세 번째 Conv 층
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Conv1d(in_channels=256, out_channels=256, kernel_size=3, padding=1),  # 네 번째 Conv 층
            nn.AdaptiveAvgPool1d(output_size=1)  # 평균 풀링으로 시퀀스 길이를 1로 축소
        )
        self.fc1 = nn.Linear(256 * 2, 1)  # 두 채널을 결합하여 처리
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # 입력이 [batch_size, channels=2, features=16, sequence_length=626] 형태임
        batch_size = x.size(0)
        
        # 채널별로 분리해서 처리할 수도 있지만, 여기서는 두 채널을 병합하여 처리
        left_channel = x[:, 0, :, :]  # [batch_size, 16, 626] 첫 번째 채널
        right_channel = x[:, 1, :, :]  # [batch_size, 16, 626] 두 번째 채널
        
        # CNN에 각각 입력
        left_output = self.cnn(left_channel)  # [batch_size, 512, 1]
        right_output = self.cnn(right_channel)  # [batch_size, 512, 1]
        
        # 두 채널의 출력을 결합
        combined_output = torch.cat((left_output, right_output), dim=1)  # [batch_size, 1024, 1]
        combined_output = combined_output.squeeze(dim=-1)  # [batch_size, 1024]
        
        # Fully connected layer에 입력
        emotion = self.fc1(combined_output)  # [batch_size, 1]
        emotion = self.sigmoid(emotion)  # Sigmoid를 통해 이진 분류
        return emotion



# RNN 모델 클래스 정의 (이진 분류)
class RNN(nn.Module):
    def __init__(self, n_mfcc=16):
        super(RNN, self).__init__()
        
        self.lstm = nn.LSTM(n_mfcc, 40, 4, batch_first=True, bidirectional=True)  # 양방향 LSTM
        self.fc = nn.Linear(160, 1)  # 두 방향의 출력(40*2)로 이진 분류를 위한 fully connected layer
        self.sigmoid = nn.Sigmoid()  # 이진 분류를 위한 Sigmoid 활성화 함수

    def forward(self, x):
        # 입력이 [batch_size, channels=2, features=16, sequence_length=626] 형태임
        # 채널별로 분리
        left_channel = x[:, 0, :, :]  # 첫 번째 채널
        right_channel = x[:, 1, :, :]  # 두 번째 채널
        
        # 각 채널을 LSTM에 입력 (입력 형태는 [batch_size, sequence_length, n_mfcc]여야 함)
        lstm_out_left, _ = self.lstm(left_channel.permute(0, 2, 1))  # [batch_size, sequence_length, features] 형태로 변환
        lstm_out_right, _ = self.lstm(right_channel.permute(0, 2, 1))
        
        # 마지막 시간 단계의 출력을 가져옵니다.
        last_output_left = lstm_out_left[:, -1, :]  # [batch_size, 80]
        last_output_right = lstm_out_right[:, -1, :]  # [batch_size, 80]
        
        # 두 채널의 출력을 결합
        combined_output = torch.cat((last_output_left, last_output_right), dim=1)  # [batch_size, 160]
        
        # Fully connected layer에 입력
        emotion = self.fc(combined_output)  # [batch_size, 1]
        emotion = self.sigmoid(emotion)  # Sigmoid를 통해 이진 분류
        return emotion  
    
# Transformer 모델 클래스 정의 (이진 분류)
class Transformer(nn.Module):
    def __init__(self, n_mfcc=16):
        super().__init__()

        self.encoder_layer = nn.TransformerEncoderLayer(d_model=n_mfcc, nhead=4, batch_first=True, dim_feedforward=512)
        self.transformer_encoder = nn.TransformerEncoder(self.encoder_layer, num_layers=4)
        self.fc = nn.Linear(160, 1)  # 두 채널의 출력을 결합하여 이진 분류를 위한 fully connected layer
        self.sigmoid = nn.Sigmoid()  # 이진 분류를 위한 Sigmoid 활성화 함수

    def forward(self, x):
        # 입력이 [batch_size, channels=2, features=16, sequence_length=626] 형태임
        # 채널별로 분리
        left_channel = x[:, 0, :, :]  # 첫 번째 채널
        right_channel = x[:, 1, :, :]  # 두 번째 채널
        
        # 각 채널을 Transformer에 입력 (입력 형태는 [batch_size, sequence_length, n_mfcc]여야 함)
        transformer_out_left = self.transformer_encoder(left_channel.permute(0, 2, 1))  # [batch_size, sequence_length, n_mfcc]
        transformer_out_right = self.transformer_encoder(right_channel.permute(0, 2, 1))
        
        # 마지막 시간 단계의 출력을 가져옵니다.
        last_output_left = transformer_out_left[:, -1, :]  # [batch_size, n_mfcc]
        last_output_right = transformer_out_right[:, -1, :]  # [batch_size, n_mfcc]
        
        # 두 채널의 출력을 결합
        combined_output = torch.cat((last_output_left, last_output_right), dim=1)  # [batch_size, 2*n_mfcc]

        # Fully connected layer에 입력
        emotion = self.fc(combined_output)  # [batch_size, 1]
        emotion = self.sigmoid(emotion)  # Sigmoid를 통해 이진 분류
        return emotion