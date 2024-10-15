import numpy as np
import librosa
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score,confusion_matrix,precision_score,recall_score,f1_score

# 멜 스펙트로그램 추출 함수
def get_melspectrogram(y, sr, n_mels, n_fft):
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, n_fft=n_fft,
                                                     hop_length=int(n_fft / 4), fmax=sr // 2)
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
    return mel_spectrogram_db

# MFCC 추출 함수
def get_mfcc(y, sr, n_mfcc, n_fft):
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc, n_fft=n_fft,
                                hop_length=int(n_fft / 4), fmax=sr // 2)
    return mfcc


def normalize_voice_len(y,normalizedLen):
    nframes=len(y)
    y = np.reshape(y,[nframes,1]).T

    if(nframes<normalizedLen):
        res=normalizedLen-nframes
        res_data=np.zeros([1,res],dtype=np.float32)
        y = np.reshape(y,[nframes,1]).T
        y=np.c_[y,res_data]
    else:
        y=y[:,0:normalizedLen]
    return y[0]

def getNearestLen(framelength,sr):
    framesize = framelength*sr

    nfftdict = {}
    lists = [32,64,128,256,512,1024,2048,4096]
    for i in lists:
        nfftdict[i] = abs(framesize - i)
    sortlist = sorted(nfftdict.items(), key=lambda x: x[1])
    framesize = int(sortlist[0][0])
    return framesize

def plot_confusion_matrix(y_true, y_pred, labels, ax=None):
    if ax is None:
        ax = plt.gca()
    # y_true와 y_pred가 1차원인지 확인
    y_true = np.array(y_true).flatten()
    y_pred = np.array(y_pred).flatten()

    num = len(labels)
    
    # confusion matrix 생성
    from sklearn.metrics import confusion_matrix
    C = confusion_matrix(y_true=y_true, y_pred=y_pred, labels=range(num))
    
    # confusion matrix 시각화
    im = ax.matshow(C, cmap=plt.cm.Reds)
    
    # matrix 값 추가
    for i in range(C.shape[0]):
        for j in range(C.shape[1]):
            ax.text(j, i, str(C[i, j]), ha='center', va='center', color='black')
    
    ax.set_ylabel('True label')
    ax.set_xlabel('Predicted label')
    
    # X축과 Y축에 라벨 추가
    ax.set_xticks(range(num))
    ax.set_yticks(range(num))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)


def get_evaluation(y_true, y_pred):
    # y_pred가 확률일 경우 0.56 기준으로 이진 분류로 변환
    y_pred = np.array(y_pred)
    print(y_pred.shape)
    y_true = np.array(y_true).flatten()  # y_true를 1차원으로 변환
    y_pred_binary = (y_pred > 0.5).astype(int)  # 확률 값을 0과 1로 변환

    print(y_true.shape)  # 확인
    print(y_pred_binary.shape)  # 확인

    # 정확도, 정밀도, 재현율, f1 스코어 계산
    acc = accuracy_score(y_true, y_pred_binary)
    precision = precision_score(y_true, y_pred_binary, average='binary')
    recall = recall_score(y_true, y_pred_binary, average='binary')
    f1 = f1_score(y_true, y_pred_binary, average='binary')

    # 소수점 3자리로 반올림
    precision = np.around(precision, 3)
    recall = np.around(recall, 3)
    f1 = np.around(f1, 3)

    return acc, precision, recall, f1

# 결과 시각화 함수에서 저장 경로 추가
def plot_fold_performance(train_losses, val_losses, val_accuracies, fold, save_path):
    plt.figure(figsize=(10, 5))
    plt.plot(train_losses, label='Train Loss')
    plt.plot(val_losses, label='Validation Loss')
    plt.title(f'Fold {fold + 1} Losses')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.savefig(save_path.replace('.png', '_loss.png'))
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(val_accuracies, label='Validation Accuracy')
    plt.title(f'Fold {fold + 1} Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.savefig(save_path.replace('.png', '_accuracy.png'))
    plt.close()

# 멜 스펙트로그램을 추출하는 함수
def get_melspectrogram(path, n_mels=128):
    y, sr = librosa.load(path, sr=16000)
    VOICE_LEN = 40000

    N_FFT = getNearestLen(0.25, sr)

    y = normalizeVoiceLen(y, VOICE_LEN)

    # 멜 스펙트로그램 계산
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, n_fft=N_FFT, hop_length=int(N_FFT/4), fmax=sr//2)
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)

    return mel_spectrogram_db