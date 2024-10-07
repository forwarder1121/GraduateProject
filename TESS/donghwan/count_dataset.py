import os

# 데이터셋 경로 설정
output_root = '/workspace/dataset/TESS'

# 감정 분류 설정
stressed_emotions = ['angry', 'disgust', 'fear', 'sad']
not_stressed_emotions = ['happy', 'neutral', 'ps']

# 폴더명에서 감정 추출하는 함수
def get_emotion_from_folder(folder_name):
    for emotion in stressed_emotions + not_stressed_emotions:
        if emotion in folder_name.lower():
            return emotion
    return None

# 데이터 개수 확인 및 출력
def count_data(output_root):
    for split in ['train', 'test']:
        split_path = os.path.join(output_root, split)
        total_count = 0
        stressed_count = 0
        not_stressed_count = 0

        for file_name in os.listdir(split_path):
            total_count += 1
            emotion = get_emotion_from_folder(file_name)
            if emotion in stressed_emotions:
                stressed_count += 1
            elif emotion in not_stressed_emotions:
                not_stressed_count += 1
            else:
                print("!!! 오류 !!!")

        print(f"{split} 데이터 총 개수: {total_count}")
        print(f"{split} - 스트레스 데이터 개수: {stressed_count}")
        print(f"{split} - 비스트레스 데이터 개수: {not_stressed_count}")

# 메인 함수
def main():
    # 데이터 개수 확인 및 출력
    count_data(output_root)

if __name__ == '__main__':
    main()