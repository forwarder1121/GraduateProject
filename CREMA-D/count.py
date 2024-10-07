import os

def count_wav_files(directory):
    count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.wav'):
                count += 1
    return count

# CREMA-D 데이터셋 경로 설정
crema_d_path = '/workspace/dataset/CREMA-D'

# .wav 파일 개수 세기
wav_file_count = count_wav_files(crema_d_path)
print(f"Total number of .wav files in CREMA-D: {wav_file_count}")
