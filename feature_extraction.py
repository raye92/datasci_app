# feature_extraction.py
import pandas as pd
import numpy as np
from scipy.stats import kurtosis
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

def extract_features(df):
    features_list = []
    grouped = df.groupby('segment')
    for seg, group in grouped:
        feature_dict = {}
        feature_dict['segment'] = seg
        for axis in ['accel_x', 'accel_y', 'accel_z', 'abs_accel']:
            data = group[axis].values
            feature_dict[f'{axis}_mean'] = np.mean(data)
            feature_dict[f'{axis}_median'] = np.median(data)
            feature_dict[f'{axis}_std'] = np.std(data)
            feature_dict[f'{axis}_kurt'] = kurtosis(data, bias=False)
        if 'activity' in group.columns:
            feature_dict['activity'] = group['activity'].mode()[0]
        features_list.append(feature_dict)
    return pd.DataFrame(features_list)

# Load training and testing data, extract features, and train the classifier.
train_df = pd.read_hdf("data.h5", key="/split/train")
test_df  = pd.read_hdf("data.h5", key="/split/test")

train_features = extract_features(train_df)
test_features = extract_features(test_df)

feature_cols = [col for col in train_features.columns if col not in ['segment', 'activity']]
scaler = StandardScaler()
train_features[feature_cols] = scaler.fit_transform(train_features[feature_cols])
test_features[feature_cols] = scaler.transform(test_features[feature_cols])

X_train = train_features[feature_cols]
y_train = train_features['activity']
X_test = test_features[feature_cols]
y_test = test_features['activity']

clf = LogisticRegression(max_iter=1000, random_state=42)
clf.fit(X_train, y_train)

if __name__ == "__main__":
    from sklearn.metrics import accuracy_score
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("test accuracy:", accuracy)

    # add the predicted activity to the test_features DataFrame.
    test_features['predicted_activity'] = y_pred

    # export the test features (with predictions) to a CSV file.
    test_features.to_csv("test.csv", index=False)
