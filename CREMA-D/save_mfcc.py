import os
import numpy as np
import torch
from tqdm import tqdm

# 필요한 라이브러리 임포트
try:
    from utils import get_mfcc  # utils 모듈에서 get_mfcc 함수 임포트
except ImportError as e:
    print(f"Could not import 'get_mfcc' from utils: {e}")

# GPU 사용 가능 여부 확인
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# MFCC 파일 저장 함수
def save_mfcc_files(input_root, output_root, n_mfcc):
    # 파일 목록 수집
    file_paths = []

    # 입력 디렉토리 존재 여부 확인
    if not os.path.exists(input_root):
        raise FileNotFoundError(f"Input directory '{input_root}' does not exist.")

    # 출력 디렉토리 존재 여부 확인, 없으면 생성
    if not os.path.exists(output_root):
        os.makedirs(output_root)

    # 오디오 파일 수집
    for file in os.listdir(input_root):
        if file.endswith('.wav'):
            file_paths.append(os.path.join(input_root, file))

    # 파일이 존재하지 않을 경우 예외 처리
    if len(file_paths) == 0:
        raise ValueError(f"No files found in directory '{input_root}'.")

    # 파일마다 MFCC 특징 추출 및 저장
    for file_path in tqdm(file_paths, desc="Extracting MFCCs", unit="file"):
        try:
            # MFCC 추출
            mfcc = get_mfcc(file_path, n_mfcc)

            # MFCC 저장 경로 설정 (파일 확장자를 .pt로 변경)
            output_file_path = os.path.join(output_root, os.path.basename(file_path).replace('.wav', '.pt'))

            # MFCC를 PyTorch 텐서 형식으로 저장
            torch.save(mfcc, output_file_path)

            print(f"Saved MFCC tensor: {output_file_path}")
        
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")



if __name__ == "__main__":
    save_mfcc_files(
        input_root='/workspace/dataset/CREMA-D/OriginalData',
        output_root='/workspace/dataset/CREMA-D/mfccData',
        n_mfcc=20
    )
    
