import os
import pandas as pd
import numpy as np
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
from Segdataset import read_test_file_list  # 필요한 경우 모듈 임포트

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
    group_cols = ['Model', 'Feature', 'Learning Rate']

    # 평균 계산 (as_index=False 사용)
    avg_df = df_pivot[df_pivot['Fold'] != 'Average'].groupby(group_cols, as_index=False)[numeric_cols].mean()

    # 집계된 결과를 Excel에 저장
    with pd.ExcelWriter(args.output_file) as writer:
        df_pivot.to_excel(writer, sheet_name='All Metrics', index=False)
        avg_df.to_excel(writer, sheet_name='Average Metrics', index=False)
        if not df_misclassified.empty:
            df_misclassified.to_excel(writer, sheet_name='Misclassified Samples', index=False)

    print(f"Aggregated results saved to {args.output_file}")

    # 테스트 데이터셋 로드 및 감정 클래스, 레벨 샘플 수 정의
    test_features, test_labels, test_filenames = read_test_file_list(
        root=args.test_data_root,
        n_mfcc=20,
        n_mels=128,
        feature_type='mfcc',
        return_filenames=True
    )

    df_test = pd.DataFrame({
        'Filename': test_filenames,
        'Label': test_labels
    })

    # 감정 클래스 및 레벨 데이터
    total_samples_class = {'ANG': 258, 'DIS': 257, 'SAD': 254, 'FEA': 248, 'HAP': 247, 'NEU': 225}
    total_samples_level = {'XX': 1220, 'HI': 90, 'LO': 90, 'MD': 89}

    # 모델별로 오분류율 계산 및 막대그래프 생성
    sns.set(style="whitegrid")

    if not df_misclassified.empty:
        # 중복된 오분류 샘플을 제거 (Filename 기준으로 중복 제거)
        df_misclassified_unique = df_misclassified.drop_duplicates(subset=['Filename', 'True Label', 'Predicted Label'])
        
        # 모델별로 그룹화
        grouped = df_misclassified_unique.groupby(['Model', 'Feature', 'Learning Rate'])
        
        for (model, feature, lr), group in grouped:
            # 감정 클래스별 오분류 수 계산
            misclassified_counts_class = group['Emotion Class'].value_counts()

            # 로그로 오분류 개수 출력
            print(f"Model: {model}, Feature: {feature}, Learning Rate: {lr}")
            print("Misclassified Emotion Counts:")
            for emotion_class, count in misclassified_counts_class.items():
                print(f"Emotion: {emotion_class}, Misclassified Count: {count}")

            # 각 감정 클래스의 오분류 비율 계산
            misclassification_rate_class = (misclassified_counts_class / pd.Series(total_samples_class).loc[misclassified_counts_class.index]) * 100

            # 감정 클래스별 오분류율 막대그래프 생성 및 저장
            plt.figure(figsize=(10, 6))
            misclassification_rate_class.sort_index().plot(kind='bar', color='steelblue')
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

            # 로그로 감정 레벨별 오분류 개수 출력
            print("Misclassified Emotion Level Counts:")
            for emotion_level, count in misclassified_counts_level.items():
                print(f"Emotion Level: {emotion_level}, Misclassified Count: {count}")

            # 감정 레벨별 오분류 비율 계산
            misclassification_rate_level = (misclassified_counts_level / pd.Series(total_samples_level).loc[misclassified_counts_level.index]) * 100
            misclassification_rate_level = misclassification_rate_level.fillna(0)

            # 감정 레벨별 오분류율 막대그래프 생성 및 저장
            plt.figure(figsize=(10, 6))
            misclassification_rate_level.sort_index().plot(kind='bar', color='lightcoral')
            plt.title(f'{model} - {feature} - LR: {lr}\nMisclassification Rate by Emotion Level')
            plt.ylabel('Misclassification Rate (%)')
            plt.xlabel('Emotion Level')
            plt.tight_layout()
            bar_chart_filename = f'misclassification_rate_emotion_level_{model}_{feature}_lr_{lr}.png'.replace('/', '_')
            plt.savefig(bar_chart_filename)
            plt.close()
            print(f"Bar chart saved: {bar_chart_filename}")




if __name__ == '__main__':
    main()
