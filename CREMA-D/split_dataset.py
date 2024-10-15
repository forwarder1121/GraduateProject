import os
import shutil
from sklearn.model_selection import train_test_split
from collections import Counter

# CREMA-D 데이터셋 경로 설정
original_data_path = '/workspace/dataset/CREMA-D/fulldata_without_XX'
train_root = '/workspace/dataset/CREMA-D/train_without_XX'
test_root = '/workspace/dataset/CREMA-D/test_without_XX'

# 폴더가 없으면 생성
os.makedirs(train_root, exist_ok=True)
os.makedirs(test_root, exist_ok=True)

# 데이터셋 로드 함수
def load_file_list(root):
    file_paths = []
    labels = []

    for subdir, _, files in os.walk(root):
        for file in files:
            if file.endswith('.wav'):
                file_path = os.path.join(subdir, file)

                # 파일 이름에서 감정 코드 추출
                emotion_code = file.split('_')[2]
                if emotion_code in ['HAP', 'NEU']:  # 비스트레스
                    label = 0
                elif emotion_code in ['ANG', 'DIS', 'SAD', 'FEA']:  # 스트레스
                    label = 1
                else:
                    continue

                file_paths.append(file_path)
                labels.append(label)

    return file_paths, labels

# 파일 로드
file_paths, labels = load_file_list(original_data_path)
print(f"Total files loaded: {len(file_paths)}")
print(f"Class distribution: {Counter(labels)}")

# Stratified 방법을 이용하여 train/test 데이터 분할
train_files, test_files, train_labels, test_labels = train_test_split(
    file_paths, labels, test_size=0.2, stratify=labels, random_state=42
)

print(f"Train files: {len(train_files)}, Test files: {len(test_files)}")
print(f"Train class distribution: {Counter(train_labels)}")
print(f"Test class distribution: {Counter(test_labels)}")

# 파일을 지정된 폴더로 복사하는 함수
def save_files(file_paths, destination):
    for file_path in file_paths:
        dest_path = os.path.join(destination, os.path.basename(file_path))
        shutil.copy(file_path, dest_path)

# train/test 데이터를 각 폴더에 저장
save_files(train_files, train_root)
save_files(test_files, test_root)

print("Data splitting and saving completed.")
