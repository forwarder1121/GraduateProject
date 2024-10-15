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

def save_to_md(df_pivot, avg_df, output_md_path):
    with open(output_md_path, 'w') as f:
        f.write("# Aggregated Results\n\n")
        
        # 모델, 학습률별로 기록
        for idx, row in df_pivot.iterrows():
            f.write(f"## Model: {row['Model']}, Feature: {row['Feature']}, Learning Rate: {row['Learning Rate']}, Fold: {row['Fold']}\n")
            f.write(f"- Accuracy: {row.get('Accuracy', 'N/A')}\n")
            f.write(f"- F1 Score: {row.get('F1 Score', 'N/A')}\n")
            f.write(f"- Precision: {row.get('Precision', 'N/A')}\n")
            f.write(f"- Recall: {row.get('Recall', 'N/A')}\n\n")

        # 평균 메트릭 기록
        f.write("## Average Metrics\n\n")
        for idx, row in avg_df.iterrows():
            f.write(f"### Model: {row['Model']}, Feature: {row['Feature']}, Learning Rate: {row['Learning Rate']}\n")
            f.write(f"- Average Accuracy: {row.get('Accuracy', 'N/A')}\n")
            f.write(f"- Average F1 Score: {row.get('F1 Score', 'N/A')}\n")
            f.write(f"- Average Precision: {row.get('Precision', 'N/A')}\n")
            f.write(f"- Average Recall: {row.get('Recall', 'N/A')}\n\n")

def main():
    parser = argparse.ArgumentParser(description="Aggregate evaluation results into a single file")
    parser.add_argument('--results_root', type=str, required=True, help='Root directory where all results are stored')
    parser.add_argument('--test_data_root', type=str, required=True, help='Root directory of the test dataset')
    parser.add_argument('--output_file', type=str, default='aggregated_results.xlsx', help='Output file name for aggregated results (Excel format)')
    parser.add_argument('--output_md_file', type=str, default='aggregated_results.md', help='Output file name for aggregated results (Markdown format)')
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
    if args.output_file.endswith('.xlsx') or args.output_file.endswith('.xls'):
        with pd.ExcelWriter(args.output_file) as writer:
            df_pivot.to_excel(writer, sheet_name='All Metrics', index=False)
            avg_df.to_excel(writer, sheet_name='Average Metrics', index=False)
            if not df_misclassified.empty:
                df_misclassified.to_excel(writer, sheet_name='Misclassified Samples', index=False)

        print(f"Aggregated results saved to {args.output_file}")
    else:
        print(f"Invalid file extension for Excel file: {args.output_file}")

    # Markdown 파일 생성
    save_to_md(df_pivot, avg_df, args.output_md_file)
    print(f"Markdown results saved to {args.output_md_file}")


if __name__ == '__main__':
    main()
