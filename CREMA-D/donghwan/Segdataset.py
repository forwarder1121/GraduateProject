import os
import numpy as np
import torch
from torch.utils.data import Dataset
from sklearn.model_selection import StratifiedKFold
import librosa
from utils import get_melspectrogram,get_mfcc,normalize_voice_len

# 감정 매핑: 파일 이름에 따라 감정 레이블 결정 (CREMA-D의 감정 코드에 맞춤)
emotion_mapping = {
    'ANG': 1, 'DIS': 1, 'FEA': 1, 'SAD': 1,  # Stressed
    'HAP': 0, 'NEU': 0  # Not Stressed
}


# 데이터셋 로드 함수
def read_test_file_list(root, n_mfcc, n_mels, feature_type, return_filenames=False, target_length=16000 * 2.5):
    features = []
    labels = []
    filenames = []

    # 오디오 파일 불러오기 및 처리
    for subdir, _, files in os.walk(root):
        for file in files:
            if file.endswith('.wav'):
                file_path = os.path.join(subdir, file)
                try:
                    # 오디오 파일 불러오기
                    y, sr = librosa.load(file_path, sr=16000)

                    # 오디오 길이 일정하게 맞추기
                    y = normalize_voice_len(y, int(target_length))

                    # N_FFT 계산
                    n_fft = 1024  # 일반적으로 사용하는 크기

                    # 피처 추출 (MFCC 또는 멜 스펙트로그램)
                    if feature_type == 'mfcc':
                        feature = get_mfcc(y=y, sr=sr, n_mfcc=n_mfcc, n_fft=n_fft)
                    elif feature_type == 'mel':
                        feature = get_melspectrogram(y=y, sr=sr, n_mels=n_mels, n_fft=n_fft)
                    else:
                        raise ValueError(f"Invalid feature type specified: {feature_type}")

                    features.append(feature)

                    # 파일 이름에서 감정 코드 추출
                    emotion_code = file.split('_')[2]
                    if emotion_code in emotion_mapping:
                        labels.append(emotion_mapping[emotion_code])
                        if return_filenames:
                            filenames.append(file)
                    else:
                        print(f"Skipping file {file_path}, no matching emotion label.")

                except Exception as e:
                    # 에러 발생 시 에러 메시지 출력
                    print(f"Error processing file {file_path}: {e}")

    if return_filenames:
        return features, labels, filenames
    else:
        return features, labels

# K-Fold 데이터셋 생성 함수
def get_kfold_data(root, feature_type, n_mfcc=20, n_mels=128, k_folds=5, random_state=1, target_length=16000 * 2.5):
    features, labels = read_test_file_list(root=root, n_mfcc=n_mfcc, n_mels=n_mels,
                                           feature_type=feature_type, target_length=target_length)

    skf = StratifiedKFold(n_splits=k_folds, shuffle=True, random_state=random_state)

    fold_data = []
    for train_index, val_index in skf.split(features, labels):
        train_features = [features[i] for i in train_index]
        val_features = [features[i] for i in val_index]
        train_labels = [labels[i] for i in train_index]
        val_labels = [labels[i] for i in val_index]
        fold_data.append((train_features, val_features, train_labels, val_labels))

    return fold_data

class SegDataset(torch.utils.data.Dataset):
    def __init__(self, features, labels, filenames=None):
        self.features = features
        self.labels = labels
        self.filenames = filenames

    def __getitem__(self, idx):
        feature = self.features[idx]
        label = self.labels[idx]
        # numpy array를 torch tensor로 변환
        feature = torch.tensor(feature, dtype=torch.float32)
        label = torch.tensor(label, dtype=torch.long)

        if self.filenames is not None:
            filename = self.filenames[idx]
            return feature, label, filename
        else:
            return feature, label

    def __len__(self):
        return len(self.features)

# 테스트용 메인 함수
if __name__ == "__main__":
    try:
        root = '/workspace/dataset/CREMA-D'
        feature_type = 'mel'  # 'mfcc' 또는 'mel'
        n_mfcc = 20
        n_mels = 128
        k_folds = 5
        target_length = 16000 * 2.5  # 2.5초 길이로 맞춤

        # K-Fold 데이터 준비
        k_folds_data = get_kfold_data(root=root, feature_type=feature_type, n_mfcc=n_mfcc,
                                      n_mels=n_mels, k_folds=k_folds, random_state=1,
                                      target_length=target_length)
        print("K-Fold 데이터 준비 완료")

        # 각 fold에 대해 데이터셋 확인
        for fold_idx, (train_features, val_features, train_labels, val_labels) in enumerate(k_folds_data):
            print(f"Fold {fold_idx + 1} | Train size: {len(train_features)}, Val size: {len(val_features)}")

            # 데이터셋 및 데이터 로더 정의
            train_dataset = SegDataset(train_features, train_labels)
            val_dataset = SegDataset(val_features, val_labels)

            print(f"Train Dataset Length: {len(train_dataset)}, Val Dataset Length: {len(val_dataset)}")

            emotion_0_count = train_labels.count(0)
            emotion_1_count = train_labels.count(1)
            print(f"Fold {fold_idx + 1}: Emotion 0 count: {emotion_0_count}, Emotion 1 count: {emotion_1_count}")

            # 샘플 데이터를 로딩하고, 그 모양과 레이블을 출력하여 확인
            if len(train_dataset) > 0:
                sample_feature, sample_label = train_dataset[0]
                print("Sample Feature shape:", sample_feature.shape)
                print("Sample Emotion Label:", sample_label)

    except Exception as e:
        print(f"An error occurred: {e}")
