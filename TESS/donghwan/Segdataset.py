import os
import numpy as np
import torch
from torch.utils.data import Dataset
from sklearn.model_selection import StratifiedKFold
from utils import get_mfcc
import librosa

# Define emotion classes

emotion_mapping = {
    'angry':1, 'disgust':1, 'fear':1, 'sad':1, # Stressed
    'happy':0, 'neutral':0, 'ps':0  # Not Stressed
}

# 오디오 길이를 일정하게 맞추는 함수
def normalize_voice_len(y, target_length):
    if len(y) < target_length:
        padding = target_length - len(y)
        y = np.pad(y, (0, padding), mode='constant')
    else:
        y = y[:target_length]
    return y

# 멜 스펙트로그램 추출 함수
def get_melspectrogram(y, sr, n_mels, n_fft):
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, n_fft=n_fft, hop_length=int(n_fft / 4), fmax=sr // 2)
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
    return mel_spectrogram_db

# MFCC 추출 함수
def get_mfcc(y, sr, n_mfcc, n_fft):
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=int(n_fft / 4), fmax=sr // 2)
    return mfcc

# 데이터셋 로드 함수
def read_test_file_list(root, feature_type, n_mfcc, n_mels, target_length=16000 * 2.5):
    mfcc_list = []
    emotion_list = []

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

                    mfcc_list.append(feature)

                    # 파일 이름에서 감정 코드 추출
                    emotion_code = file.split('_')[-1].split('.')[0].lower()
                    if emotion_code in emotion_mapping:
                        emotion_list.append(emotion_mapping[emotion_code])
                    else:
                        print(f"Skipping file {file_path}, no matching emotion label.")

                except Exception as e:
                    # 에러 발생 시 에러 메시지 출력
                    print(f"Error processing file {file_path}: {e}")

    return mfcc_list, emotion_list


# K-Fold 데이터셋 생성 함수
def get_kfold_data(root, feature_type, n_mfcc=20, n_mels=128, k_folds=5, random_state=1, target_length=16000 * 2.5):
    mfcc_list, emotion_list = read_test_file_list(root=root, feature_type=feature_type, n_mfcc=n_mfcc, n_mels=n_mels, target_length=target_length)

    skf = StratifiedKFold(n_splits=k_folds, shuffle=True, random_state=random_state)

    fold_data = []
    for train_index, val_index in skf.split(mfcc_list, emotion_list):
        mfcc_train = [mfcc_list[i] for i in train_index]
        mfcc_val = [mfcc_list[i] for i in val_index]
        emotion_train = [emotion_list[i] for i in train_index]
        emotion_val = [emotion_list[i] for i in val_index]
        fold_data.append((mfcc_train, mfcc_val, emotion_train, emotion_val))

    return fold_data

# 데이터셋 클래스
class SegDataset(Dataset):
    def __init__(self, mfcc_list, emotion_list):
        self.mfcc = mfcc_list
        self.emotion = emotion_list
        print(f"Dataset loaded with {len(self.mfcc)} samples.")

    def __getitem__(self, idx):
        mfcc = self.mfcc[idx]
        emotion = self.emotion[idx]

        # Convert to Torch tensor and adjust dimensions
        mfcc = torch.from_numpy(np.array(mfcc)).type(torch.FloatTensor).transpose(1, 0)  # [n_mfcc, time] -> [time, n_mfcc]
        emotion = torch.tensor(emotion, dtype=torch.long)

        return mfcc, emotion

    def __len__(self):
        return len(self.mfcc)