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
        # 파일명도 반환하도록 수정
        test_features, test_labels, test_filenames = read_test_file_list(
            root='/workspace/dataset/CREMA-D/test',
            n_mfcc=args.n_mfcc,
            n_mels=args.n_mels,
            feature_type='mfcc',
            return_filenames=True
        )
        in_channels = args.n_mfcc
    elif args.feature_type == 'mel':
        # 파일명도 반환하도록 수정
        test_features, test_labels, test_filenames = read_test_file_list(
            root='/workspace/dataset/CREMA-D/test',
            n_mfcc=args.n_mfcc,
            n_mels=args.n_mels,
            feature_type='mel',
            return_filenames=True
        )
        in_channels = args.n_mels  # 수정: mel 피처일 경우 n_mels 사용

    # test_set 생성 시 filenames도 전달
    test_set = SegDataset(test_features, test_labels, filenames=test_filenames)
    test_loader = DataLoader(test_set, batch_size=1, drop_last=False, num_workers=args.num_workers)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # 모델 초기화
    if args.model_type == 'CNN':
        model = CNN(in_channels=in_channels)
    elif args.model_type == 'VGG_CNN':
        model = VGG_CNN(in_channels=in_channels)
    elif args.model_type == 'ResNetCNN':
        model = ResNetCNN(in_channels=in_channels)
    else:
        raise ValueError(f"Invalid model type specified: {args.model_type}")

    model = model.to(device)

    all_metrics = []

    # 잘못 분류된 샘플 정보를 저장할 리스트
    misclassified_samples = []

    for fold in range(args.n_folds):
        # 모델 파라미터 로드
        checkpoint_path = os.path.join(checkpoint_dir, f'fold_{fold + 1}_best_epoch_lr_{args.learning_rate}.pth')
        if not os.path.isfile(checkpoint_path):
            print(f"Checkpoint not found for fold {fold + 1} at {checkpoint_path}")
            continue  # 해당 폴드 스킵
        model.load_state_dict(torch.load(checkpoint_path, map_location=device))
        model.eval()

        output_emotion_list = []
        label_emotion_list = []
        filename_list = []

        # 감정 레벨별 결과 저장용 딕셔너리
        results_per_emotion_level = {'LO': {'preds': [], 'labels': []},
                                     'MD': {'preds': [], 'labels': []},
                                     'HI': {'preds': [], 'labels': []},
                                     'XX': {'preds': [], 'labels': []}}

        with torch.no_grad():
            for features, emotion, filename in test_loader:
                features, emotion = features.to(device), emotion.to(device)

               
                output_emotion = model(features)
                output_emotion = torch.sigmoid(output_emotion)
                predicted_emotion = (output_emotion > 0.5).float()

                output_emotion_list.append(predicted_emotion.cpu().numpy())
                label_emotion_list.append(emotion.cpu().numpy())
                filename_list.append(filename[0])

                # 파일명에서 감정 레벨 추출
                filename_str = filename[0]  # batch_size=1이므로 첫 번째 요소만 사용
                parts = filename_str.split('_')
                emotion_class = parts[2]  # 감정 클래스 (예: 'ANG')
                emotion_level_part = parts[-1]  # 예: 'MD.wav'
                emotion_level = emotion_level_part.split('.')[0]  # 'MD'

                # 잘못 분류된 샘플 저장
                if predicted_emotion.item() != emotion.item():
                    misclassified_samples.append({
                        'filename': filename_str,
                        'emotion_class': emotion_class,
                        'emotion_level': emotion_level,
                        'true_label': int(emotion.item()),
                        'predicted_label': int(predicted_emotion.item())
                    })

                # 감정 레벨별로 결과 저장
                if emotion_level in results_per_emotion_level:
                    results_per_emotion_level[emotion_level]['preds'].append(predicted_emotion.cpu().numpy())
                    results_per_emotion_level[emotion_level]['labels'].append(emotion.cpu().numpy())
                else:
                    print(f"Unknown emotion level: {emotion_level} in file {filename_str}")

        output_emotion_list = np.vstack(output_emotion_list)[:, 0]
        label_emotion_list = np.vstack(label_emotion_list)[:, 0]

        # 평가
        acc, precision, recall, f1 = get_evaluation(label_emotion_list, output_emotion_list)
        all_metrics.append((acc, precision, recall, f1))

        # 결과 출력
        print(f"Fold {fold + 1} - Accuracy: {acc}, Precision: {precision}, Recall: {recall}, F1 Score: {f1}")

        # 전체 데이터에 대한 혼동 행렬 생성 및 저장
        plot_confusion_matrix(label_emotion_list, output_emotion_list, labels=['NotStressed', 'Stressed'])
        plt.title(f'Confusion Matrix - Fold {fold + 1}')
        plt.savefig(os.path.join(result_dir, f'confusion_matrix_fold_{fold + 1}.png'))
        plt.close()

        # 각 감정 레벨별 혼동 행렬 생성 및 저장 (하나의 이미지로 결합)
        fig, axs = plt.subplots(2, 2, figsize=(12, 10))
        emotion_levels = ['LO', 'MD', 'HI', 'XX']
        axs = axs.flatten()

        for idx, emotion_level in enumerate(emotion_levels):
            results = results_per_emotion_level[emotion_level]
            if len(results['labels']) == 0:
                axs[idx].axis('off')  # 데이터가 없을 경우 축을 비움
                continue

            preds = np.vstack(results['preds'])[:, 0]
            labels = np.vstack(results['labels'])[:, 0]

            # 혼동 행렬 생성
            plot_confusion_matrix(labels, preds, labels=['NotStressed', 'Stressed'], ax=axs[idx])
            axs[idx].set_title(f'Emotion Level {emotion_level}')

        plt.tight_layout()
        combined_cm_path = os.path.join(result_dir, f'combined_confusion_matrix_fold_{fold + 1}.png')
        plt.savefig(combined_cm_path)
        plt.close()

    if all_metrics:
        # 평균값 계산
        avg_metrics = np.mean(all_metrics, axis=0)
        print(f"Average - Accuracy: {avg_metrics[0]}, Precision: {avg_metrics[1]}, Recall: {avg_metrics[2]}, F1 Score: {avg_metrics[3]}")

        # Markdown 파일에 결과 기록
        md_path = os.path.join(result_dir, 'evaluation_results.md')
        with open(md_path, 'w') as f:
            f.write(f"# Evaluation Results for {args.model_type} with {args.feature_type} Features\n")
            f.write(f"## Learning Rate: {args.learning_rate}\n\n")
            for fold_idx, metrics in enumerate(all_metrics):
                acc, precision, recall, f1 = metrics
                f.write(f"### Fold {fold_idx + 1}\n")
                f.write(f"- Accuracy: {acc:.3f}\n")
                f.write(f"- Precision: {precision:.3f}\n")
                f.write(f"- Recall: {recall:.3f}\n")
                f.write(f"- F1 Score: {f1:.3f}\n\n")

            f.write(f"## Average Metrics\n")
            f.write(f"- Average Accuracy: {avg_metrics[0]:.3f}\n")
            f.write(f"- Average Precision: {avg_metrics[1]:.3f}\n")
            f.write(f"- Average Recall: {avg_metrics[2]:.3f}\n")
            f.write(f"- Average F1 Score: {avg_metrics[3]:.3f}\n\n")

            # 잘못 분류된 샘플 정보 기록
            f.write(f"## Misclassified Samples\n")
            f.write("| Filename | Emotion Class | Emotion Level | True Label | Predicted Label |\n")
            f.write("|----------|---------------|---------------|------------|-----------------|\n")
            for sample in misclassified_samples:
                f.write(f"| {sample['filename']} | {sample['emotion_class']} | {sample['emotion_level']} | {sample['true_label']} | {sample['predicted_label']} |\n")

        print(f"Results saved to {md_path}")
    else:
        print("No metrics to report.")

if __name__ == '__main__':
    main()
