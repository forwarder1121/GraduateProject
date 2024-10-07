import os
import numpy as np
import torch
import argparse
from torch.utils.data import DataLoader
from utils import plot_confusion_matrix, get_evaluation
from models import CNN, ResNetCNN, VGG_CNN
from Segdataset import SegDataset, read_test_file_list
import matplotlib.pyplot as plt

# CUDA 장치 설정
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def main():
    # argparse를 사용하여 명령줄 인자를 정의합니다.
    parser = argparse.ArgumentParser(description="Test model with specified parameters and features")
    parser.add_argument('--learning_rate', type=float, required=True, help='Learning rate used during training')
    parser.add_argument('--model_type', type=str, required=True, choices=['CNN', 'VGG_CNN', 'ResNetCNN'], help='Model type to use for testing')
    parser.add_argument('--feature_type', type=str, required=True, choices=['mfcc', 'mel'], help='Feature type used during training')
    parser.add_argument('--n_mfcc', type=int, default=20, help='Number of MFCC features')
    parser.add_argument('--n_mels', type=int, default=128, help='Number of Mel spectrogram features')
    parser.add_argument('--n_folds', type=int, default=5, help='Number of folds for KFold validation')
    parser.add_argument('--num_workers', type=int, default=16, help='Number of worker processes for data loading')
    
    args = parser.parse_args()

    # 경로 설정
    base_dir = f'/workspace/UndergraduateResearchAssistant/GraduateProject/code/CREMA-D/donghwan/{args.feature_type}/{args.model_type}/lr_{args.learning_rate}'
    checkpoint_dir = os.path.join(base_dir, 'checkpoints')
    result_dir = os.path.join(base_dir, 'test_results')
    os.makedirs(result_dir, exist_ok=True)

    # 데이터셋 로드
    if args.feature_type == 'mfcc':
        test_features, test_labels = read_test_file_list(root='/workspace/dataset/CREMA-D/test', n_mfcc=args.n_mfcc, n_mels=args.n_mels, feature_type='mfcc')
        in_channels = args.n_mfcc
    elif args.feature_type == 'mel':                                                
        test_features, test_labels = read_test_file_list(root='/workspace/dataset/CREMA-D/test', n_mfcc=args.n_mfcc, n_mels=args.n_mels, feature_type='mel')
        in_channels = args.n_mels  # 수정: mel 피처일 경우 n_mels 사용


    test_set = SegDataset(test_features, test_labels)
    test_loader = DataLoader(test_set, batch_size=1, drop_last=True, num_workers=args.num_workers)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # 모델 초기화 
    if args.model_type == 'CNN':
        model = CNN(in_channels=in_channels)
    elif args.model_type == 'VGG_CNN':
        model = VGG_CNN(in_channels=in_channels)
    elif args.model_type == 'ResNetCNN':
        model = ResNetCNN(in_channels=in_channels).to(device)
    else:
        raise ValueError(f"Invalid model type specified: {args.model_type}")

    
    model = model.to(device)

    all_metrics = []

    for fold in range(args.n_folds):
        model.load_state_dict(torch.load(os.path.join(checkpoint_dir, f'fold_{fold + 1}_best_epoch_lr_{args.learning_rate}.pth'), map_location=device))
        model.eval()

        output_emotion_list = []
        label_emotion_list = []

        with torch.no_grad():
            for features, emotion in test_loader:
                features, emotion = features.to(device), emotion.to(device)
                output_emotion = model(features)
                output_emotion = torch.sigmoid(output_emotion)
                predicted_emotion = (output_emotion > 0.5).float()

                output_emotion_list.append(predicted_emotion.cpu().numpy())
                label_emotion_list.append(emotion.cpu().numpy())

        output_emotion_list = np.vstack(output_emotion_list)[:, 0]
        label_emotion_list = np.vstack(label_emotion_list)[:, 0]

        # 평가
        acc, precision, recall, f1 = get_evaluation(label_emotion_list, output_emotion_list)
        all_metrics.append((acc, precision, recall, f1))

        # 결과 출력
        print(f"Fold {fold + 1} - Accuracy: {acc}, Precision: {precision}, Recall: {recall}, F1 Score: {f1}")

        # Confusion Matrix 생성 및 저장
        plot_confusion_matrix(label_emotion_list, output_emotion_list, labels=['NotStressed', 'Stressed'])
        plt.title(f'Confusion Matrix - Fold {fold + 1}')
        plt.savefig(os.path.join(result_dir, f'confusion_matrix_fold_{fold + 1}.png'))
        plt.close()

    # 평균값 계산
    avg_metrics = np.mean(all_metrics, axis=0)
    print(f"Average - Accuracy: {avg_metrics[0]}, Precision: {avg_metrics[1]}, Recall: {avg_metrics[2]}, F1 Score: {avg_metrics[3]}")

    # Markdown 파일에 결과 기록
    md_path = os.path.join(result_dir, 'evaluation_results.md')
    with open(md_path, 'w') as f:
        f.write(f"# Evaluation Results for {args.model_type} with {args.feature_type} Features\n")
        f.write(f"## Learning Rate: {args.learning_rate}\n\n")
        for fold in range(args.n_folds):
            acc, precision, recall, f1 = all_metrics[fold]
            f.write(f"### Fold {fold + 1}\n")
            f.write(f"- Accuracy: {acc:.3f}\n")
            f.write(f"- Precision: {precision:.3f}\n")
            f.write(f"- Recall: {recall:.3f}\n")
            f.write(f"- F1 Score: {f1:.3f}\n\n")

        f.write(f"## Average Metrics\n")
        f.write(f"- Average Accuracy: {avg_metrics[0]:.3f}\n")
        f.write(f"- Average Precision: {avg_metrics[1]:.3f}\n")
        f.write(f"- Average Recall: {avg_metrics[2]:.3f}\n")
        f.write(f"- Average F1 Score: {avg_metrics[3]:.3f}\n")

    print(f"Results saved to {md_path}")

if __name__ == '__main__':
    main()
