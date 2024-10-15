import matplotlib.pyplot as plt
import numpy as np

# 감정 레벨과 오분류율 데이터
emotion_levels = ['HI', 'LO', 'MD', 'XX']
misclassification_rates = [5.0, 4.2, 2.8, 3.6]  # 예시 데이터 (임의의 오분류율)

# 감정 레벨별 정확도 (알맞게 분류한 비율)
accuracies = {
    'LO': 75.56,
    'MD': 80.90,
    'HI': 78.89,
    'XX': 76.31
}

# 막대 그래프 생성
plt.figure(figsize=(8, 6))
bars = plt.bar(emotion_levels, misclassification_rates, color='lightcoral')

# 그래프 제목과 라벨 설정
plt.title('VGG_CNN - mfcc - LR: 3e-05\nMisclassification Rate by Emotion Level', fontsize=14)
plt.xlabel('Emotion Level', fontsize=12)
plt.ylabel('Misclassification Rate (%)', fontsize=12)

# 정확도 정보를 그래프 아래에 추가
accuracy_text = f"각 감정 레벨당 알맞게 분류한 비율(정확도):\nLO: {accuracies['LO']}%, MD: {accuracies['MD']}%, HI: {accuracies['HI']}%, XX: {accuracies['XX']}%"
plt.figtext(0.5, -0.1, accuracy_text, ha='center', fontsize=12)

# 그래프 출력
plt.tight_layout()
plt.show()
