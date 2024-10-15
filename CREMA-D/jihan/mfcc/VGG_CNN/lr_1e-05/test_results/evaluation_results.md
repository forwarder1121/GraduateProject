# Evaluation Results for VGG_CNN with mfcc Features
## Learning Rate: 1e-05

### Fold 1
- Accuracy: 0.847
- Precision: 0.954
- Recall: 0.849
- F1 Score: 0.899

### Fold 2
- Accuracy: 0.796
- Precision: 0.927
- Recall: 0.808
- F1 Score: 0.863

### Fold 3
- Accuracy: 0.847
- Precision: 0.932
- Recall: 0.872
- F1 Score: 0.901

### Fold 4
- Accuracy: 0.799
- Precision: 0.956
- Recall: 0.785
- F1 Score: 0.862

### Fold 5
- Accuracy: 0.792
- Precision: 0.950
- Recall: 0.781
- F1 Score: 0.857

## Average Metrics
- Average Accuracy: 0.816
- Average Precision: 0.944
- Average Recall: 0.819
- Average F1 Score: 0.876

## Misclassified Samples
| Filename | Emotion Class | Emotion Level | True Label | Predicted Label |
|----------|---------------|---------------|------------|-----------------|
| 1042_IEO_FEA_MD.wav | FEA | MD | 1 | 0 |
| 1067_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1007_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1072_IEO_SAD_LO.wav | SAD | LO | 1 | 0 |
| 1079_IEO_ANG_HI.wav | ANG | HI | 1 | 0 |
| 1066_IEO_ANG_HI.wav | ANG | HI | 1 | 0 |
| 1060_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1037_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1088_IEO_HAP_LO.wav | HAP | LO | 0 | 1 |
| 1049_IEO_HAP_HI.wav | HAP | HI | 0 | 1 |
| 1039_IEO_ANG_MD.wav | ANG | MD | 1 | 0 |
| 1083_IEO_HAP_MD.wav | HAP | MD | 0 | 1 |
| 1003_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1050_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1077_IEO_DIS_HI.wav | DIS | HI | 1 | 0 |
| 1064_IEO_HAP_LO.wav | HAP | LO | 0 | 1 |
| 1069_IEO_ANG_MD.wav | ANG | MD | 1 | 0 |
| 1010_IEO_SAD_HI.wav | SAD | HI | 1 | 0 |
| 1079_IEO_DIS_HI.wav | DIS | HI | 1 | 0 |
| 1024_IEO_ANG_MD.wav | ANG | MD | 1 | 0 |
| 1070_IEO_HAP_LO.wav | HAP | LO | 0 | 1 |
| 1021_IEO_HAP_HI.wav | HAP | HI | 0 | 1 |
| 1063_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1018_IEO_HAP_LO.wav | HAP | LO | 0 | 1 |
| 1065_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1031_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1010_IEO_SAD_LO.wav | SAD | LO | 1 | 0 |
| 1088_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1023_IEO_FEA_LO.wav | FEA | LO | 1 | 0 |
| 1034_IEO_SAD_MD.wav | SAD | MD | 1 | 0 |
| 1072_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1003_IEO_DIS_LO.wav | DIS | LO | 1 | 0 |
| 1074_IEO_HAP_MD.wav | HAP | MD | 0 | 1 |
| 1077_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1069_IEO_FEA_MD.wav | FEA | MD | 1 | 0 |
| 1070_IEO_FEA_LO.wav | FEA | LO | 1 | 0 |
| 1039_IEO_FEA_MD.wav | FEA | MD | 1 | 0 |
| 1040_ITH_SAD_X.wav | SAD | X | 1 | 0 |
| 1014_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1007_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1071_IEO_ANG_MD.wav | ANG | MD | 1 | 0 |
| 1002_IEO_HAP_MD.wav | HAP | MD | 0 | 1 |
| 1014_IEO_HAP_MD.wav | HAP | MD | 0 | 1 |
| 1060_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1037_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1003_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1088_IEO_HAP_LO.wav | HAP | LO | 0 | 1 |
| 1080_IEO_HAP_MD.wav | HAP | MD | 0 | 1 |
| 1036_IEO_HAP_HI.wav | HAP | HI | 0 | 1 |
| 1035_IEO_HAP_HI.wav | HAP | HI | 0 | 1 |
| 1050_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1077_IEO_DIS_HI.wav | DIS | HI | 1 | 0 |
| 1064_IEO_HAP_LO.wav | HAP | LO | 0 | 1 |
| 1069_IEO_ANG_MD.wav | ANG | MD | 1 | 0 |
| 1040_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1050_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1032_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1079_IEO_DIS_HI.wav | DIS | HI | 1 | 0 |
| 1024_IEO_ANG_MD.wav | ANG | MD | 1 | 0 |
| 1063_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1078_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1065_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1046_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1031_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1027_IEO_SAD_HI.wav | SAD | HI | 1 | 0 |
| 1019_IEO_FEA_LO.wav | FEA | LO | 1 | 0 |
| 1032_IEO_DIS_LO.wav | DIS | LO | 1 | 0 |
| 1008_IEO_FEA_MD.wav | FEA | MD | 1 | 0 |
| 1027_IEO_DIS_HI.wav | DIS | HI | 1 | 0 |
| 1079_IEO_FEA_MD.wav | FEA | MD | 1 | 0 |
| 1043_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1068_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1088_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1039_IEO_HAP_MD.wav | HAP | MD | 0 | 1 |
| 1023_IEO_FEA_LO.wav | FEA | LO | 1 | 0 |
| 1034_IEO_SAD_MD.wav | SAD | MD | 1 | 0 |
| 1072_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1074_IEO_HAP_MD.wav | HAP | MD | 0 | 1 |
| 1077_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1074_IEO_FEA_MD.wav | FEA | MD | 1 | 0 |
| 1051_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1027_IEO_HAP_MD.wav | HAP | MD | 0 | 1 |
| 1078_IEO_SAD_HI.wav | SAD | HI | 1 | 0 |
| 1089_IEO_HAP_HI.wav | HAP | HI | 0 | 1 |
| 1049_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1070_IEO_FEA_LO.wav | FEA | LO | 1 | 0 |
| 1074_IEO_HAP_HI.wav | HAP | HI | 0 | 1 |
| 1077_IEO_ANG_MD.wav | ANG | MD | 1 | 0 |
| 1041_IEO_SAD_MD.wav | SAD | MD | 1 | 0 |
| 1035_IEO_HAP_MD.wav | HAP | MD | 0 | 1 |
| 1073_IEO_DIS_LO.wav | DIS | LO | 1 | 0 |
| 1040_ITH_SAD_X.wav | SAD | X | 1 | 0 |
| 1041_IEO_HAP_LO.wav | HAP | LO | 0 | 1 |
| 1014_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1007_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1071_IEO_ANG_MD.wav | ANG | MD | 1 | 0 |
| 1079_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1002_IEO_HAP_MD.wav | HAP | MD | 0 | 1 |
| 1005_IEO_ANG_HI.wav | ANG | HI | 1 | 0 |
| 1014_IEO_HAP_MD.wav | HAP | MD | 0 | 1 |
| 1060_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1003_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1088_IEO_HAP_LO.wav | HAP | LO | 0 | 1 |
| 1080_IEO_HAP_MD.wav | HAP | MD | 0 | 1 |
| 1036_IEO_HAP_HI.wav | HAP | HI | 0 | 1 |
| 1083_IEO_HAP_MD.wav | HAP | MD | 0 | 1 |
| 1035_IEO_HAP_HI.wav | HAP | HI | 0 | 1 |
| 1050_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1077_IEO_DIS_HI.wav | DIS | HI | 1 | 0 |
| 1064_IEO_HAP_LO.wav | HAP | LO | 0 | 1 |
| 1069_IEO_ANG_MD.wav | ANG | MD | 1 | 0 |
| 1079_IEO_DIS_HI.wav | DIS | HI | 1 | 0 |
| 1024_IEO_ANG_MD.wav | ANG | MD | 1 | 0 |
| 1070_IEO_HAP_LO.wav | HAP | LO | 0 | 1 |
| 1021_IEO_HAP_HI.wav | HAP | HI | 0 | 1 |
| 1063_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1018_IEO_HAP_LO.wav | HAP | LO | 0 | 1 |
| 1078_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1013_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1065_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1031_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1008_IEO_FEA_MD.wav | FEA | MD | 1 | 0 |
| 1027_IEO_DIS_HI.wav | DIS | HI | 1 | 0 |
| 1068_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1023_IEO_FEA_LO.wav | FEA | LO | 1 | 0 |
| 1034_IEO_SAD_MD.wav | SAD | MD | 1 | 0 |
| 1072_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1036_IEO_HAP_MD.wav | HAP | MD | 0 | 1 |
| 1074_IEO_HAP_MD.wav | HAP | MD | 0 | 1 |
| 1077_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1004_IEO_FEA_LO.wav | FEA | LO | 1 | 0 |
| 1070_IEO_FEA_LO.wav | FEA | LO | 1 | 0 |
| 1077_IEO_ANG_MD.wav | ANG | MD | 1 | 0 |
| 1035_IEO_HAP_MD.wav | HAP | MD | 0 | 1 |
| 1040_ITH_SAD_X.wav | SAD | X | 1 | 0 |
| 1014_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1007_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1071_IEO_ANG_MD.wav | ANG | MD | 1 | 0 |
| 1079_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1002_IEO_HAP_MD.wav | HAP | MD | 0 | 1 |
| 1005_IEO_ANG_HI.wav | ANG | HI | 1 | 0 |
| 1018_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1007_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1087_IEO_DIS_LO.wav | DIS | LO | 1 | 0 |
| 1066_IEO_ANG_HI.wav | ANG | HI | 1 | 0 |
| 1060_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1088_IEO_HAP_LO.wav | HAP | LO | 0 | 1 |
| 1049_IEO_HAP_HI.wav | HAP | HI | 0 | 1 |
| 1080_IEO_HAP_MD.wav | HAP | MD | 0 | 1 |
| 1056_IEO_FEA_MD.wav | FEA | MD | 1 | 0 |
| 1083_IEO_HAP_MD.wav | HAP | MD | 0 | 1 |
| 1050_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1077_IEO_DIS_HI.wav | DIS | HI | 1 | 0 |
| 1064_IEO_HAP_LO.wav | HAP | LO | 0 | 1 |
| 1042_IEO_HAP_MD.wav | HAP | MD | 0 | 1 |
| 1069_IEO_ANG_MD.wav | ANG | MD | 1 | 0 |
| 1040_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1070_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1032_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1079_IEO_DIS_HI.wav | DIS | HI | 1 | 0 |
| 1020_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1058_IEO_SAD_HI.wav | SAD | HI | 1 | 0 |
| 1024_IEO_ANG_MD.wav | ANG | MD | 1 | 0 |
| 1063_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1087_IEO_ANG_MD.wav | ANG | MD | 1 | 0 |
| 1030_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1078_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1015_IEO_DIS_LO.wav | DIS | LO | 1 | 0 |
| 1072_IEO_DIS_HI.wav | DIS | HI | 1 | 0 |
| 1013_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1065_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1046_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1031_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1008_IEO_FEA_MD.wav | FEA | MD | 1 | 0 |
| 1027_IEO_DIS_HI.wav | DIS | HI | 1 | 0 |
| 1068_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1088_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1023_IEO_FEA_LO.wav | FEA | LO | 1 | 0 |
| 1072_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1046_IEO_DIS_HI.wav | DIS | HI | 1 | 0 |
| 1077_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1074_IEO_FEA_MD.wav | FEA | MD | 1 | 0 |
| 1058_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1049_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1069_IEO_FEA_MD.wav | FEA | MD | 1 | 0 |
| 1070_IEO_FEA_LO.wav | FEA | LO | 1 | 0 |
| 1077_IEO_ANG_MD.wav | ANG | MD | 1 | 0 |
| 1022_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1041_IEO_HAP_LO.wav | HAP | LO | 0 | 1 |
| 1014_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1007_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1071_IEO_ANG_MD.wav | ANG | MD | 1 | 0 |
| 1050_IEO_FEA_MD.wav | FEA | MD | 1 | 0 |
| 1079_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1002_IEO_HAP_MD.wav | HAP | MD | 0 | 1 |
| 1028_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1042_IEO_FEA_MD.wav | FEA | MD | 1 | 0 |
| 1007_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1062_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1079_IEO_ANG_HI.wav | ANG | HI | 1 | 0 |
| 1066_IEO_ANG_HI.wav | ANG | HI | 1 | 0 |
| 1060_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1037_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1062_IEO_ANG_MD.wav | ANG | MD | 1 | 0 |
| 1088_IEO_HAP_LO.wav | HAP | LO | 0 | 1 |
| 1049_IEO_HAP_HI.wav | HAP | HI | 0 | 1 |
| 1083_IEO_HAP_MD.wav | HAP | MD | 0 | 1 |
| 1067_IEO_ANG_HI.wav | ANG | HI | 1 | 0 |
| 1050_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1077_IEO_DIS_HI.wav | DIS | HI | 1 | 0 |
| 1064_IEO_HAP_LO.wav | HAP | LO | 0 | 1 |
| 1069_IEO_ANG_MD.wav | ANG | MD | 1 | 0 |
| 1040_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1070_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1050_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1032_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1079_IEO_DIS_HI.wav | DIS | HI | 1 | 0 |
| 1058_IEO_SAD_HI.wav | SAD | HI | 1 | 0 |
| 1024_IEO_ANG_MD.wav | ANG | MD | 1 | 0 |
| 1070_IEO_HAP_LO.wav | HAP | LO | 0 | 1 |
| 1021_IEO_HAP_HI.wav | HAP | HI | 0 | 1 |
| 1063_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1018_IEO_HAP_LO.wav | HAP | LO | 0 | 1 |
| 1078_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1072_IEO_DIS_HI.wav | DIS | HI | 1 | 0 |
| 1065_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1046_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1031_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1008_IEO_FEA_MD.wav | FEA | MD | 1 | 0 |
| 1043_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1068_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1088_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1072_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1046_IEO_DIS_HI.wav | DIS | HI | 1 | 0 |
| 1077_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1004_IEO_FEA_LO.wav | FEA | LO | 1 | 0 |
| 1074_IEO_FEA_MD.wav | FEA | MD | 1 | 0 |
| 1089_IEO_HAP_HI.wav | HAP | HI | 0 | 1 |
| 1049_IEO_FEA_HI.wav | FEA | HI | 1 | 0 |
| 1069_IEO_FEA_MD.wav | FEA | MD | 1 | 0 |
| 1070_IEO_FEA_LO.wav | FEA | LO | 1 | 0 |
| 1035_IEO_FEA_MD.wav | FEA | MD | 1 | 0 |
| 1042_IEO_HAP_HI.wav | HAP | HI | 0 | 1 |
| 1039_IEO_FEA_MD.wav | FEA | MD | 1 | 0 |
| 1077_IEO_ANG_MD.wav | ANG | MD | 1 | 0 |
| 1022_IEO_DIS_MD.wav | DIS | MD | 1 | 0 |
| 1073_IEO_DIS_LO.wav | DIS | LO | 1 | 0 |
| 1040_ITH_SAD_X.wav | SAD | X | 1 | 0 |
| 1014_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1007_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
| 1071_IEO_ANG_MD.wav | ANG | MD | 1 | 0 |
| 1079_IEO_ANG_LO.wav | ANG | LO | 1 | 0 |
