#!/bin/bash

# 학습률 배열 정의
learning_rates=("1e-5" "3e-5" "5e-5")

# 피처 타입 배열 정의
feature_types=("mfcc")

# 모델 배열 정의
models=("ResNetCNN" "VGG_CNN" "CNN")

# train.py 파일을 학습률, 피처 타입, 모델 타입에 대해 실행하고 그에 맞는 test.py 실행
for lr in "${learning_rates[@]}"; do
    for feature_type in "${feature_types[@]}"; do
        for model in "${models[@]}"; do
            echo "학습 시작 - 모델: $model, 피처 타입: $feature_type, 학습률: $lr"
            
            # train.py 실행
            python train.py --learning_rate $lr --model_type $model --feature_type $feature_type

            echo "학습 완료 - 모델: $model, 피처 타입: $feature_type, 학습률: $lr"
            echo "테스트 시작 - 모델: $model, 피처 타입: $feature_type, 학습률: $lr"

            # test.py 실행 - 학습과 동일한 하이퍼파라미터로 모델을 평가
            python test.py --learning_rate $lr --model_type $model --feature_type $feature_type

            echo "테스트 완료 - 모델: $model, 피처 타입: $feature_type, 학습률: $lr"
        done
    done
done

echo "모든 학습 및 테스트 작업이 완료되었습니다."

# 모든 결과를 종합하는 aggregate_results.py 실행
echo "결과 종합 시작"
python aggregate_results.py --test_data_root /workspace/dataset/CREMA-D/test --results_root /workspace/UndergraduateResearchAssistant/GraduateProject/code/CREMA-D/donghwan/ --output_file aggregated_results.md
echo "결과 종합 완료 - 결과는 aggregated_results.md 파일에 저장되었습니다."
