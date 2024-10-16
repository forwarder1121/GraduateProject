## 폴더 구조

```plaintext
/workspace/UndergraduateResearchAssistant/GraduateProject/code/CREMA-D/donghwan/
  ├── mfcc/
  │   ├── ResNetCNN/
  │   │   ├── lr_1e-5/
  │   │   │   ├── checkpoints/
  │   │   │   │   ├── fold_1_best_epoch_lr_1e-5.pth
  │   │   │   │   ├── fold_2_best_epoch_lr_1e-5.pth
  │   │   │   │   └── ...
  │   │   │   ├── result/
  │   │   │   │   ├── fold_1_performance_lr_1e-5.png
  │   │   │   │   └── ...
  │   │   │   ├── test_results/
  │   │   │   │   ├── confusion_matrix_fold_1.png
  │   │   │   │   ├── evaluation_results.md
  │   │   │   │   └── ...
  │   │   ├── lr_3e-5/
  │   │   └── lr_5e-5/
  │   ├── VGG_CNN/
  │   ├── CNN/
  ├── mel/
  │   ├── ResNetCNN/
  │   ├── VGG_CNN/
  │   ├── CNN/
  ├── aggregated_results.md
  ├── train.py
  ├── test.py
  └── aggregate_results.py
```

## 폴더 설명

- `mfcc/`와 `mel/`: MFCC와 Mel-spectrogram 특징을 기반으로 한 모델 결과가 각각 저장된 폴더입니다.
  - `ResNetCNN/`, `VGG_CNN/`, `CNN/`: 각 모델에 대한 학습 및 테스트 결과 폴더.
  - `lr_1e-5/`, `lr_3e-5/`, `lr_5e-5/`: 학습률별 실험 결과가 저장된 폴더.
    - `checkpoints/`: 각 폴드에 대한 모델 가중치 파일이 저장된 폴더 (`.pth` 파일).
    - `result/`: 각 폴드의 학습 결과 그래프 (`.png` 파일).
    - `test_results/`: 각 폴드의 혼동 행렬 및 평가 결과 (`evaluation_results.md` 파일).
- `aggregated_results.md`: 모든 실험의 결과를 종합하여 요약한 파일.
- `train.py`: 모델 학습을 수행하는 스크립트.
- `test.py`: 학습된 모델을 테스트하는 스크립트.
- `aggregate_results.py`: 모든 폴드와 학습률에 대한 결과를 종합하여 요약하는 스크립트.


## MFCC 조기종료 적용 (10.14)

## Hyperparameters and Training Environment

| Argument        | Type      | Default Value  | Description                                             |
|-----------------|-----------|----------------|---------------------------------------------------------|
| **learning_rate** | float     | 1e-4           | Learning rate for the optimizer                          |
| **model_type**    | str       | 'VGG_CNN'      | Model type to use (choices: ['CNN', 'VGG_CNN', 'ResNetCNN']) |
| **feature_type**  | str       | 'mfcc'         | Feature type to use (choices: ['mfcc'])                   |
| **n_mfcc**        | int       | 20             | Number of MFCC features to extract                       |
| **n_mels**        | int       | 128            | Number of Mel spectrogram features to extract            |
| **epoch**         | int       | 500            | Number of training epochs                                |
| **batch_size**    | int       | 64             | Batch size for training                                  |
| **num_workers**   | int       | 16             | Number of worker processes for data loading              |
| **n_splits**      | int       | 5              | Number of splits for KFold cross-validation              |

### Early Stopping Logic
The early stopping mechanism is introduced to halt training when the model stops improving based on validation performance, reducing overfitting and saving computational resources.



| 모델        | 학습률  | Fold 1 | Fold 2 | Fold 3 | Fold 4 | Fold 5 | 평균 정확도 | 평균 F1 스코어 | 평균 정밀도 | 평균 재현율 |
|-------------|---------|--------|--------|--------|--------|--------|-------------|----------------|-------------|-------------|
| CNN         | 1e-05   | 0.738  | 0.731  | 0.750  | 0.731  | 0.737  | 0.7374      | 0.7934         | 0.8582      | 0.7376      |
| CNN         | 3e-05   | 0.730  | 0.729  | 0.757  | 0.728  | 0.745  | 0.7378      | 0.7936         | 0.8586      | 0.7376      |
| CNN         | 5e-05   | 0.747  | 0.743  | 0.736  | 0.740  | 0.731  | 0.7394      | 0.7942         | 0.8628      | 0.7360      |
| ResNetCNN   | 1e-05   | 0.748  | 0.772  | 0.769  | 0.783  | 0.760  | 0.7664      | 0.8206         | 0.8636      | 0.7816      |
| ResNetCNN   | 3e-05   | 0.788  | 0.793  | 0.753  | 0.770  | 0.766  | 0.7740      | 0.8256         | 0.8730      | 0.7838      |
| ResNetCNN   | 5e-05   | 0.766  | 0.764  | 0.754  | 0.770  | 0.774  | 0.7656      | 0.8156         | 0.8810      | 0.7594      |
| VGG_CNN     | 1e-05   | 0.766  | 0.754  | 0.774  | 0.777  | 0.779  | 0.7700      | 0.8210         | 0.8748      | 0.7740      |
| VGG_CNN     | 3e-05   | 0.753  | 0.770  | 0.776  | 0.755  | 0.774  | 0.7656      | 0.8178         | 0.8722      | 0.7700      |
| VGG_CNN     | 5e-05   | 0.764  | 0.776  | 0.754  | 0.774  | 0.726  | 0.7588      | 0.8096         | 0.8762      | 0.7550      |




---

## 실험 결과 요약 (MFCC Feature)

| 모델      | 학습률  | Fold 1 | Fold 2 | Fold 3 | Fold 4 | Fold 5 | 평균 정확도 | 평균 F1 스코어 | 평균 정밀도 | 평균 재현율 |
|-----------|---------|--------|--------|--------|--------|--------|-------------|---------------|-------------|-------------|
| CNN       | 1e-05   | 0.649  | 0.632  | 0.649  | 0.656  | 0.643  | 0.646       | 0.718         | 0.787       | 0.660       |
| CNN       | 3e-05   | 0.674  | 0.663  | 0.680  | 0.664  | 0.673  | 0.671       | 0.733         | 0.823       | 0.660       |
| CNN       | 5e-05   | 0.686  | 0.699  | 0.697  | 0.682  | 0.682  | 0.689       | 0.753         | 0.823       | 0.694       |
| ResNetCNN | 1e-05   | 0.682  | 0.709  | 0.685  | 0.686  | 0.672  | 0.687       | 0.748         | 0.830       | 0.682       |
| ResNetCNN | 3e-05   | 0.752  | 0.762  | 0.742  | 0.739  | 0.741  | 0.747       | 0.802         | 0.863       | 0.750       |
| ResNetCNN | 5e-05   | 0.769  | 0.770  | 0.751  | 0.751  | 0.776  | 0.763       | 0.816         | 0.868       | 0.771       |
| VGG_CNN   | 1e-05   | 0.706  | 0.724  | 0.713  | 0.717  | 0.711  | 0.714       | 0.771         | 0.849       | 0.707       |
| VGG_CNN   | 3e-05   | 0.767  | 0.760  | 0.741  | 0.770  | 0.761  | 0.760       | 0.814         | 0.866       | 0.767       |
| VGG_CNN   | 5e-05   | 0.768  | 0.764  | 0.774  | 0.758  | 0.767  | 0.766       | 0.820         | 0.866       | 0.779       |




## 실험 결과 요약 (Mel Feature)

| 모델      | 학습률  | Fold 1 | Fold 2 | Fold 3 | Fold 4 | Fold 5 | 평균 정확도 | 평균 F1 스코어 | 평균 정밀도 | 평균 재현율 |
|-----------|---------|--------|--------|--------|--------|--------|-------------|---------------|-------------|-------------|
| CNN       | 1e-05   | 0.671  | 0.661  | 0.651  | 0.668  | 0.661  | 0.662       | 0.726         | 0.814       | 0.656       |
| CNN       | 3e-05   | 0.681  | 0.694  | 0.669  | 0.696  | 0.669  | 0.682       | 0.738         | 0.845       | 0.655       |
| CNN       | 5e-05   | 0.702  | 0.684  | 0.697  | 0.689  | 0.715  | 0.698       | 0.754         | 0.846       | 0.682       |
| ResNetCNN | 1e-05   | 0.685  | 0.686  | 0.676  | 0.674  | 0.691  | 0.682       | 0.738         | 0.846       | 0.655       |
| ResNetCNN | 3e-05   | 0.727  | 0.717  | 0.749  | 0.736  | 0.717  | 0.729       | 0.783         | 0.862       | 0.718       |
| ResNetCNN | 5e-05   | 0.747  | 0.769  | 0.721  | 0.735  | 0.741  | 0.743       | 0.800         | 0.851       | 0.755       |
| VGG_CNN   | 1e-05   | 0.707  | 0.709  | 0.697  | 0.692  | 0.695  | 0.700       | 0.756         | 0.850       | 0.681       |
| VGG_CNN   | 3e-05   | 0.721  | 0.743  | 0.731  | 0.732  | 0.736  | 0.733       | 0.790         | 0.850       | 0.739       |
| VGG_CNN   | 5e-05   | 0.735  | 0.729  | 0.718  | 0.730  | 0.717  | 0.726       | 0.782         | 0.856       | 0.720       |

### 표 설명
- **모델**: 사용된 모델 (CNN, ResNetCNN, VGG_CNN).
- **학습률**: 학습률 (1e-5, 3e-5, 5e-5).
- **Fold 1~5**: 각 폴드별 정확도 결과.
- **평균 정확도, F1 스코어, 정밀도, 재현율**: 각 모델과 학습률에 대한 평균 성능 지표.

위 표는 MFCC 및 Mel 특징을 사용한 실험 결과를 요약한 것입니다.    
각 학습률 및 모델 조합에 대해 5개의 폴드를 사용하여 교차 검증을 수행하였으며, 평균 성능 지표가 요약되어 있습니다.
