import os
import sys
import numpy as np
import torch
import torch.optim as optim
import torch.nn as nn
import argparse
from torch.utils.data import DataLoader
from models import CNN, VGG_CNN, ResNetCNN
from utils import plot_fold_performance
from Segdataset import SegDataset, get_kfold_data

# CUDA 장치 설정
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

def main():
    # argparse를 사용하여 명령줄 인자를 정의합니다.
    parser = argparse.ArgumentParser(description="Train model with specified hyperparameters and features")
    parser.add_argument('--learning_rate', type=float, default=1e-4, help='Learning rate for the optimizer')
    parser.add_argument('--model_type', type=str, default='VGG_CNN', choices=['CNN', 'VGG_CNN', 'ResNetCNN'], help='Model type to use')
    parser.add_argument('--feature_type', type=str, default='mfcc', choices=['mfcc', 'mel'], help='Feature type to use: mfcc or mel')
    parser.add_argument('--n_mfcc', type=int, default=20, help='Number of MFCC features to extract')
    parser.add_argument('--n_mels', type=int, default=128, help='Number of Mel spectrogram features to extract')
    parser.add_argument('--epoch', type=int, default=100, help='Number of training epochs')
    parser.add_argument('--batch_size', type=int, default=1028, help='Batch size for training')
    parser.add_argument('--num_workers', type=int, default=16, help='Number of worker processes for data loading')
    parser.add_argument('--n_splits', type=int, default=5, help='Number of splits for KFold cross-validation')

    args = parser.parse_args()

    # CUDA 사용 가능 여부 확인
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # 저장 경로 설정
    base_dir = f'/workspace/UndergraduateResearchAssistant/GraduateProject/code/TESS/donghwan/{args.feature_type}/{args.model_type}/lr_{args.learning_rate}'
    save_root = os.path.join(base_dir, 'checkpoints')
    result_root = os.path.join(base_dir, 'result')
    os.makedirs(save_root, exist_ok=True)
    os.makedirs(result_root, exist_ok=True)

    # 데이터셋 로딩 (한 번만 로드)
    if args.feature_type == 'mfcc':
        fold_data = get_kfold_data(root='/workspace/dataset/TESS/train', n_mfcc=args.n_mfcc, feature_type='mfcc')
        in_channels = args.n_mfcc
    elif args.feature_type == 'mel':
        fold_data = get_kfold_data(root='/workspace/dataset/TESS/train', n_mels=args.n_mels, feature_type='mel')
        in_channels = args.n_mels
    else:
        raise ValueError(f"Invalid feature type specified: {args.feature_type}")

    # 학습 및 검증 루프 시작
    for fold, (train_features, val_features, train_emotion, val_emotion) in enumerate(fold_data):
        print(f"Fold {fold + 1}/{args.n_splits}")

        # 모델 초기화 (폴드가 바뀔 때마다 새로 초기화)
        if args.model_type == 'CNN':
            model = CNN(in_channels=in_channels).to(device)
        elif args.model_type == 'VGG_CNN':
            model = VGG_CNN(in_channels=in_channels).to(device)
        elif args.model_type == 'ResNetCNN':
            model = ResNetCNN(in_channels=in_channels).to(device)
        else:
            raise ValueError(f"Invalid model type specified: {args.model_type}")

        # 학습/검증 데이터셋 및 로더 생성
        train_set = SegDataset(train_features, train_emotion)
        val_set = SegDataset(val_features, val_emotion)

        train_loader = DataLoader(train_set, batch_size=args.batch_size, shuffle=True, drop_last=True, num_workers=args.num_workers, pin_memory=True)
        val_loader = DataLoader(val_set, batch_size=args.batch_size, shuffle=False, drop_last=False, num_workers=args.num_workers, pin_memory=True)

        # 각 fold에 따라 pos_weight 동적으로 설정
        num_pos = sum(em == 1 for em in train_emotion)
        num_neg = sum(em == 0 for em in train_emotion)
        pos_weight = torch.tensor([num_neg / num_pos]).to(device) if num_pos > 0 else torch.tensor([1.0]).to(device)

        # 손실 함수 및 옵티마이저 선언
        criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight).to(device)
        optimizer = torch.optim.Adam(model.parameters(), lr=args.learning_rate)

        # 현재 폴드 값들 저장
        train_losses = []
        val_losses = []
        val_accuracies = []

        best_val_loss = float('inf')
        best_epoch = 0

        # 에포크 루프
        for epo in range(args.epoch):
            # 모델 학습 모드 전환
            model.train()
            train_loss = 0

            # 학습 루프
            for features, emotion in train_loader:
                features, emotion = features.to(device), emotion.to(device)
                optimizer.zero_grad()

                # 모델 예측 및 손실 계산
                output_emotion = model(features)
                loss = criterion(output_emotion[:, 0].squeeze(), emotion.float())

                # 역전파 및 옵티마이저 스텝
                loss.backward()
                optimizer.step()

                train_loss += loss.item()

            # 검증 루프
            model.eval()
            val_loss = 0
            correct_emotion = 0
            total = 0

            with torch.no_grad():
                for features, emotion in val_loader:
                    features, emotion = features.to(device), emotion.to(device)
                    output_emotion = model(features)
                    loss = criterion(output_emotion[:, 0].squeeze(), emotion.float())
                    val_loss += loss.item()

                    predicted_emotion = (torch.sigmoid(output_emotion[:, 0]) > 0.5).float()
                    correct_emotion += (predicted_emotion == emotion).sum().item()
                    total += emotion.size(0)

            # 정확도 계산
            val_accuracy = correct_emotion / total if total > 0 else 0.0

            # 결과 출력
            print(f"Fold {fold + 1} | Epoch {epo} | Train Loss: {train_loss / len(train_loader)} | Val Loss: {val_loss / len(val_loader)} | Val Accuracy: {val_accuracy}")

            # 모델 저장
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                best_epoch = epo
                torch.save(model.state_dict(), os.path.join(save_root, f'fold_{fold + 1}_best_epoch_lr_{args.learning_rate}.pth'))

            train_losses.append(train_loss / len(train_loader))
            val_losses.append(val_loss / len(val_loader))
            val_accuracies.append(val_accuracy)

        print(f"Fold {fold + 1} best epoch: {best_epoch}")

        # 각 폴드의 학습 손실, 검증 손실 및 정확도 시각화 및 저장
        result_path = os.path.join(result_root, f'fold_{fold + 1}_performance_lr_{args.learning_rate}.png')
        plot_fold_performance(train_losses, val_losses, val_accuracies, fold, result_path)

if __name__ == "__main__":
    main()