import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis, iqr
from sklearn.preprocessing import StandardScaler

def extract_features(df):
    # list to store feature dictionaries
    features_list = []

    # group by 'segment'
    grouped = df.groupby('segment')

    for seg, group in grouped:
        feature_dict = {}
        feature_dict['segment'] = seg

        # compute features for each axis
        for axis in ['accel_x', 'accel_y', 'accel_z', 'abs_accel']:
            data = group[axis].values

            # statistical features
            # feature_dict[f'{axis}_max'] = np.max(data)
            # feature_dict[f'{axis}_min'] = np.min(data)
            feature_dict[f'{axis}_mean'] = np.mean(data)
            feature_dict[f'{axis}_median'] = np.median(data)
            feature_dict[f'{axis}_std'] = np.std(data)
            # feature_dict[f'{axis}_var'] = np.var(data)
            # feature_dict[f'{axis}_range'] = np.max(data) - np.min(data)
            # feature_dict[f'{axis}_skew'] = skew(data, bias=False)
            feature_dict[f'{axis}_kurt'] = kurtosis(data, bias=False)
            # feature_dict[f'{axis}_iqr'] = iqr(data)

        # set activity to mode of group
        feature_dict['activity'] = group['activity'].mode()[0]

        features_list.append(feature_dict)

    return pd.DataFrame(features_list)

# load training and testing data
train_df = pd.read_hdf("data.h5", key="/split/train")
test_df  = pd.read_hdf("data.h5", key="/split/test")

# print("Test DataFrame shape:", test_df.shape)
# print(test_df.head())
# print(test_df.info())
# print("Unique segments in test_df:", test_df['segment'].nunique())


train_features = extract_features(train_df)
test_features = extract_features(test_df)

# list columns to normalize (exclude segment and activity)
feature_cols = [col for col in train_features.columns if col not in ['segment', 'activity']]

scaler = StandardScaler()
train_features[feature_cols] = scaler.fit_transform(train_features[feature_cols])
test_features[feature_cols] = scaler.transform(test_features[feature_cols])

import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import learning_curve

# separate features and labels
X_train = train_features[feature_cols]
y_train = train_features['activity']
X_test = test_features[feature_cols]
y_test = test_features['activity']

# initialize logistic regression model
clf = LogisticRegression(max_iter=1000, random_state=42)

# train model on full training set
clf.fit(X_train, y_train)

# predict on test set and compute accuracy
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("test accuracy:", accuracy)
