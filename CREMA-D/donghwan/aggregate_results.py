import os
import pandas as pd
import numpy as np
import argparse
import matplotlib.pyplot as plt
import seaborn as sns

# 필요한 경우, 데이터셋 로드에 필요한 모듈 임포트
from Segdataset import read_test_file_list

def parse_evaluation_results(md_file_path):
    with open(md_file_path, 'r') as f:
        lines = f.readlines()
    
    metrics = []
    misclassified_samples = []
    fold = None
    in_misclassified_section = False
    for line in lines:
        line = line.strip()
        if line.startswith('# Evaluation Results'):
            # 모델과 피처 타입 추출
            parts = line.split(' for ')[1].split(' with ')
            model_type = parts[0]
            feature_type = parts[1].replace(' Features', '')
        elif line.startswith('## Learning Rate:'):
            learning_rate = line.split(':')[1].strip()
        elif line.startswith('### Fold'):
            fold = line.replace('### Fold ', '')
            in_misclassified_section = False
        elif line.startswith('## Average Metrics'):
            fold = 'Average'
            in_misclassified_section = False
        elif line.startswith('## Misclassified Samples'):
            in_misclassified_section = True
        elif in_misclassified_section and line.startswith('|') and not line.startswith('| Filename') and '---' not in line:
            # 잘못 분류된 샘플 파싱
            parts = [p.strip() for p in line.strip().strip('|').split('|')]
            if len(parts) >= 5:
                try:
                    true_label = int(parts[3])
                    predicted_label = int(parts[4])
                    misclassified_samples.append({
                        'Model': model_type,
                        'Feature': feature_type,
                        'Learning Rate': learning_rate,
                        'Fold': fold,
                        'Filename': parts[0],
                        'Emotion Class': parts[1],
                        'Emotion Level': parts[2],
                        'True Label': true_label,
                        'Predicted Label': predicted_label
                    })
                except ValueError as e:
                    print(f"Parsing error in line: {line}")
                    continue
        elif line.startswith('- '):
            if fold is not None:
                metric_name, value = line[2:].split(': ')
                metrics.append({
                    'Model': model_type,
                    'Feature': feature_type,
                    'Learning Rate': learning_rate,
                    'Fold': fold,
                    'Metric': metric_name.strip(),
                    'Value': float(value)
                })
    return metrics, misclassified_samples

def main():
    parser = argparse.ArgumentParser(description="Aggregate evaluation results into a single file")
    parser.add_argument('--results_root', type=str, required=True, help='Root directory where all results are stored')
    parser.add_argument('--test_data_root', type=str, required=True, help='Root directory of the test dataset')
    parser.add_argument('--output_file', type=str, default='aggregated_results.xlsx', help='Output file name for aggregated results (Excel format)')
    args = parser.parse_args()

    all_metrics = []
    all_misclassified_samples = []

    for root, dirs, files in os.walk(args.results_root):
        for file in files:
            if file == 'evaluation_results.md':
                md_file_path = os.path.join(root, file)
                metrics, misclassified_samples = parse_evaluation_results(md_file_path)
                all_metrics.extend(metrics)
                all_misclassified_samples.extend(misclassified_samples)

    # 메트릭이 있는지 확인
    if len(all_metrics) == 0:
        print("No metrics found to aggregate.")
        return

    df_metrics = pd.DataFrame(all_metrics)
    df_misclassified = pd.DataFrame(all_misclassified_samples)

    # 'Learning Rate'를 float으로 변환하여 정렬 가능하게 함
    df_metrics['Learning Rate'] = df_metrics['Learning Rate'].astype(float)
    if not df_misclassified.empty:
        df_misclassified['Learning Rate'] = df_misclassified['Learning Rate'].astype(float)

    # 메트릭에 대한 피벗 테이블 생성
    df_pivot = df_metrics.pivot_table(
        index=['Model', 'Feature', 'Learning Rate', 'Fold'],
        columns='Metric',
        values='Value'
    ).reset_index()

    # 수치형 컬럼만 선택
    numeric_cols = df_pivot.select_dtypes(include=[np.number]).columns

    # 그룹화할 컬럼
    group_cols = ['Model', 'Feature', 'Learning Rate']

    # 평균 계산 (as_index=False 사용)
    avg_df = df_pivot[df_pivot['Fold'] != 'Average'].groupby(group_cols, as_index=False)[numeric_cols].mean()

    # 집계된 결과를 Excel에 저장
    with pd.ExcelWriter(args.output_file) as writer:
        df_pivot.to_excel(writer, sheet_name='All Metrics', index=False)

        avg_df.to_excel(writer, sheet_name='Average Metrics', index=False)

        # 잘못 분류된 샘플 저장
        if not df_misclassified.empty:
            df_misclassified.to_excel(writer, sheet_name='Misclassified Samples', index=False)

    print(f"Aggregated results saved to {args.output_file}")

    # 테스트 데이터셋 로드 (전체 샘플 수 계산을 위해)
    # 필요한 파라미터는 실험에 맞게 조정하세요
    test_features, test_labels, test_filenames = read_test_file_list(
        root=args.test_data_root,
        n_mfcc=20,  # 또는 필요한 n_mfcc 값
        n_mels=128,  # 또는 필요한 n_mels 값
        feature_type='mfcc',  # 또는 'mel' 등
        return_filenames=True
    )

    # 테스트 데이터프레임 생성
    df_test = pd.DataFrame({
        'Filename': test_filenames,
        'Label': test_labels
    })

    # 파일명에서 감정 클래스와 감정 레벨 추출
    emotion_classes = []
    emotion_levels = []
    for filename in df_test['Filename']:
        parts = filename.split('_')
        emotion_class = parts[2]  # 예: 'ANG'
        emotion_level_part = parts[-1]  # 예: 'MD.wav'
        emotion_level = emotion_level_part.split('.')[0]  # 'MD'
        emotion_classes.append(emotion_class)
        emotion_levels.append(emotion_level)

    df_test['Emotion Class'] = emotion_classes
    df_test['Emotion Level'] = emotion_levels

    # 전체 샘플 수 계산
    total_samples_class = df_test['Emotion Class'].value_counts().to_dict()
    total_samples_level = df_test['Emotion Level'].value_counts().to_dict()

    # 모델별로 오분류율 계산 및 막대그래프 생성
    sns.set(style="whitegrid")

    if not df_misclassified.empty:
        # 모델별로 그룹화
        grouped = df_misclassified.groupby(['Model', 'Feature', 'Learning Rate'])
        for (model, feature, lr), group in grouped:
            # 감정 클래스별 오분류 수 계산
            misclassified_counts_class = group['Emotion Class'].value_counts()
            # 전체 샘플 수에서 퍼센트 계산
            misclassification_rate_class = (misclassified_counts_class / pd.Series(total_samples_class)) * 100

            # 감정 클래스별 오분류율 막대그래프 생성
            plt.figure(figsize=(10, 6))
            misclassification_rate_class.sort_index().plot(kind='bar')
            plt.title(f'{model} - {feature} - LR: {lr}\nMisclassification Rate by Emotion Class')
            plt.ylabel('Misclassification Rate (%)')
            plt.xlabel('Emotion Class')
            plt.tight_layout()
            bar_chart_filename = f'misclassification_rate_emotion_class_{model}_{feature}_lr_{lr}.png'.replace('/', '_')
            plt.savefig(bar_chart_filename)
            plt.close()
            print(f"Bar chart saved: {bar_chart_filename}")

            # 감정 레벨별 오분류 수 계산
            misclassified_counts_level = group['Emotion Level'].value_counts()
            # 전체 샘플 수에서 퍼센트 계산
            misclassification_rate_level = (misclassified_counts_level / pd.Series(total_samples_level)) * 100

            # 감정 레벨별 오분류율 막대그래프 생성
            plt.figure(figsize=(10, 6))
            misclassification_rate_level.sort_index().plot(kind='bar')
            plt.title(f'{model} - {feature} - LR: {lr}\nMisclassification Rate by Emotion Level')
            plt.ylabel('Misclassification Rate (%)')
            plt.xlabel('Emotion Level')
            plt.tight_layout()
            bar_chart_filename = f'misclassification_rate_emotion_level_{model}_{feature}_lr_{lr}.png'.replace('/', '_')
            plt.savefig(bar_chart_filename)
            plt.close()
            print(f"Bar chart saved: {bar_chart_filename}")

    # 기존의 평균 메트릭 플롯 (영어로 유지)
    metrics_list = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
    for metric in metrics_list:
        plt.figure(figsize=(10, 6))
        sns.barplot(
            data=avg_df,
            x='Model',
            y=metric,
            hue='Feature'
        )
        plt.title(f'Average {metric} by Model and Feature')
        plt.ylabel(metric)
        plt.xlabel('Model')
        plt.legend(title='Feature Type')
        plt.tight_layout()
        plot_filename = f'average_{metric.lower().replace(" ", "_")}.png'
        plt.savefig(plot_filename)
        plt.close()
        print(f"Plot saved: {plot_filename}")

    # 기존의 파이 차트 생성 부분은 필요에 따라 유지하거나 제거할 수 있습니다.

if __name__ == '__main__':
    main()
