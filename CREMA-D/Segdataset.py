import os
import numpy as np
import torch
from torch.utils.data import Dataset
from sklearn.model_selection import StratifiedKFold
import librosa

# 감정 매핑: 파일 이름에 따라 감정 레이블 결정 (CREMA-D의 감정 코드에 맞춤)
emotion_mapping = {
    'ANG': 1, 'DIS': 1, 'FEA': 1, 'SAD': 1,  # Stressed
    'HAP': 0, 'NEU': 0  # Not Stressed
}

# 오디오 길이를 일정하게 맞추는 함수
def normalize_voice_len(y, target_length):
    if len(y) < target_length:
        padding = target_length - len(y)
        y = np.pad(y, (0, padding), mode='constant')
    else:
        y = y[:target_length]
    return y

# 데이터셋 로드 함수
def read_test_file_list(root, n_mfcc, target_length=16000 * 2.5):
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

                    # MFCC 추출
                    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
                    mfcc_list.append(mfcc)

                    # 파일 이름에서 감정 코드 추출
                    emotion_code = file.split('_')[2]
                    if emotion_code in emotion_mapping:
                        emotion_list.append(emotion_mapping[emotion_code])
                    else:
                        print(f"Skipping file {file_path}, no matching emotion label.")

                except Exception as e:
                    # 에러 발생 시 에러 메시지 출력
                    print(f"Error processing file {file_path}: {e}")

    return mfcc_list, emotion_list


# K-Fold 데이터셋 생성 함수
def get_kfold_data(root, n_mfcc, k_folds=5, random_state=1, target_length=16000 * 2.5):
    mfcc_list, emotion_list = read_test_file_list(root=root, n_mfcc=n_mfcc, target_length=target_length)

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

# 테스트용 메인 함수
if __name__ == "__main__":
    try:
        root = '/workspace/dataset/CREMA-D'
        n_mfcc = 20
        k_folds = 5
        target_length = 16000 * 2.5  # 2.5초 길이로 맞춤

        # K-Fold 데이터 준비
        k_folds_data = get_kfold_data(root=root, n_mfcc=n_mfcc, k_folds=k_folds, random_state=1, target_length=target_length)
        print("K-Fold 데이터 준비 완료")

        # 각 fold에 대해 데이터셋 확인
        for fold_idx, (train_mfcc, val_mfcc, train_emotion, val_emotion) in enumerate(k_folds_data):
            print(f"Fold {fold_idx + 1} | Train size: {len(train_mfcc)}, Val size: {len(val_mfcc)}")

            # 데이터셋 및 데이터 로더 정의
            train_dataset = SegDataset(train_mfcc, train_emotion)
            val_dataset = SegDataset(val_mfcc, val_emotion)

            print(f"Train Dataset Length: {len(train_dataset)}, Val Dataset Length: {len(val_dataset)}")

            emotion_0_count = train_emotion.count(0)
            emotion_1_count = train_emotion.count(1)
            print(f"Fold {fold_idx + 1}: Emotion 0 count: {emotion_0_count}, Emotion 1 count: {emotion_1_count}")

            # 샘플 데이터를 로딩하고, 그 모양과 레이블을 출력하여 확인
            if len(train_dataset) > 0:
                sample_mfcc, sample_emotion = train_dataset[0]
                print("Sample MFCC shape:", sample_mfcc.shape)
                print("Sample Emotion Label:", sample_emotion)

    except Exception as e:
        print(f"An error occurred: {e}")
