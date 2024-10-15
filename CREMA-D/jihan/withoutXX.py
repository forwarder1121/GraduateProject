import os
import shutil

# 원본 데이터 경로와 복사할 경로 지정
source_dir = '/workspace/dataset/CREMA-D/OriginalData'
target_dir = '/workspace/dataset/CREMA-D/fulldata_without_XX'

# 타겟 디렉터리가 없으면 생성
os.makedirs(target_dir, exist_ok=True)

# 디렉터리 내의 파일들을 반복하며 처리
for filename in os.listdir(source_dir):
    # 파일명이 'XX'를 포함하지 않는 경우만 복사
    if 'XX' not in filename:
        # 원본 파일 경로와 타겟 파일 경로
        src_path = os.path.join(source_dir, filename)
        dst_path = os.path.join(target_dir, filename)
        
        # 파일 복사
        shutil.copy(src_path, dst_path)

print("XX 제외한 파일 복사가 완료되었습니다.")
