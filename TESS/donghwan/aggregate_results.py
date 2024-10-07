import os
import pandas as pd
import argparse

def parse_evaluation_results(md_file_path):
    with open(md_file_path, 'r') as f:
        lines = f.readlines()
    
    metrics = {}
    fold = None
    for line in lines:
        line = line.strip()
        if line.startswith('# Evaluation Results'):
            # 모델 정보 추출
            parts = line.split(' for ')[1].split(' with ')
            model_type = parts[0]
            feature_type = parts[1].replace(' Features', '')
        elif line.startswith('## Learning Rate:'):
            learning_rate = line.split(':')[1].strip()
        elif line.startswith('### Fold'):
            fold = line.replace('### Fold ', '')
        elif line.startswith('- '):
            if fold is not None:
                metric_name, value = line[2:].split(': ')
                key = (model_type, feature_type, learning_rate, fold, metric_name)
                metrics[key] = float(value)
    return metrics

def main():
    parser = argparse.ArgumentParser(description="Aggregate evaluation results into a single file")
    parser.add_argument('--results_root', type=str, required=True, help='Root directory where all results are stored')
    parser.add_argument('--output_file', type=str, default='aggregated_results.csv', help='Output file name for aggregated results')
    args = parser.parse_args()

    all_metrics = {}

    for root, dirs, files in os.walk(args.results_root):
        for file in files:
            if file == 'evaluation_results.md':
                md_file_path = os.path.join(root, file)
                metrics = parse_evaluation_results(md_file_path)
                all_metrics.update(metrics)

    # 데이터프레임 생성
    data = []
    for key, value in all_metrics.items():
        model_type, feature_type, learning_rate, fold, metric_name = key
        data.append({
            'Model': model_type,
            'Feature': feature_type,
            'Learning Rate': learning_rate,
            'Fold': fold,
            'Metric': metric_name,
            'Value': value
        })

    # 'data' 리스트가 비어있는지 확인하여 오류가 발생하지 않도록 합니다.
    if len(data) == 0:
        print("No metrics found to aggregate.")
        return

    df = pd.DataFrame(data)

    # 피벗 테이블을 만들 때, 가능한 빈 데이터와 관련된 문제를 방지합니다.
    try:
        df_pivot = df.pivot_table(index=['Model', 'Feature', 'Learning Rate', 'Fold'], columns='Metric', values='Value').reset_index()
    except KeyError as e:
        print(f"KeyError: {e}")
        print("Make sure the 'Value' column is correctly populated in the dataframe.")
        return

    # CSV 파일로 저장
    df_pivot.to_csv(args.output_file, index=False)
    print(f"Aggregated results saved to {args.output_file}")

if __name__ == '__main__':
    main()
