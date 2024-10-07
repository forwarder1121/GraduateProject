import os
import shutil
from sklearn.model_selection import StratifiedShuffleSplit

# 데이터셋 경로 설정
data_root = '/workspace/dataset/TESS/originalDataset'
output_root = '/workspace/dataset/TESS'

# 감정 분류 설정
stressed_emotions = ['angry', 'disgust', 'fear', 'sad']
not_stressed_emotions = ['happy', 'neutral', 'pleasant_surprise', 'pleasant_surprised']

# 폴더명에서 감정 추출하는 함수
def get_emotion_from_folder(folder_name):
    for emotion in stressed_emotions + not_stressed_emotions:
        if emotion in folder_name.lower():
            return emotion
    return None

# 데이터 분류 함수
def classify_data(data_root):
    all_files = []
    labels = []

    for folder_name in os.listdir(data_root):
        emotion = get_emotion_from_folder(folder_name)
        if emotion is None:
            continue

        folder_path = os.path.join(data_root, folder_name)
        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.wav'):
                    file_path = os.path.join(folder_path, file_name)
                    all_files.append(file_path)
                    if emotion in stressed_emotions:
                        labels.append(1)  # Stressed
                    else:
                        labels.append(0)  # Not Stressed

    return all_files, labels

# 데이터 분할 및 저장
def split_and_save_data(files, labels, output_root, test_size=0.2):
    sss = StratifiedShuffleSplit(n_splits=1, test_size=test_size, random_state=42)

    for train_index, test_index in sss.split(files, labels):
        train_files = [files[i] for i in train_index]
        test_files = [files[i] for i in test_index]

    # 데이터 저장
    for split, split_files in zip(['train', 'test'], [train_files, test_files]):
        split_path = os.path.join(output_root, split)
        os.makedirs(split_path, exist_ok=True)

        for file in split_files:
            dest_file = os.path.join(split_path, os.path.basename(file))
            shutil.copy2(file, dest_file)

# 메인 함수
def main():
    all_files, labels = classify_data(data_root)

    # 데이터 분할 및 저장
    split_and_save_data(all_files, labels, output_root)

if __name__ == '__main__':
    main()
