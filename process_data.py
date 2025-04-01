import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from visualization import plot_comparison
window_size = 8  # window size

def load_and_label(file_path, activity_label):
    # read csv
    df = pd.read_csv(file_path)
    # rename columns
    df.rename(columns={
        "Time (s)": "time",
        "Linear Acceleration x (m/s^2)": "accel_x",
        "Linear Acceleration y (m/s^2)": "accel_y",
        "Linear Acceleration z (m/s^2)": "accel_z",
        "Absolute acceleration (m/s^2)": "abs_accel"
    }, inplace=True)
    # add activity column (0 walking, 1 jumping)
    df["activity"] = activity_label
    return df

def preprocess_data(df, hdf5_file, member_name):
    raw_data = df.copy()

    # apply moving average filter
    filtered_data = df.copy()
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    for col in numeric_cols:
        filtered_data[col] = filtered_data[col].rolling(window=window_size, min_periods=1).mean()

    # save datasets to hdf5
    with pd.HDFStore(hdf5_file, mode='a') as store:
        store.put(f'/raw/{member_name}', raw_data, format='table')
        store.put(f'/processed/{member_name}', filtered_data, format='table')
    print(f"data saved to {hdf5_file} with keys '/raw/{member_name}' and '/processed/{member_name}'.")

    return raw_data, filtered_data

if __name__ == '__main__':
    # list of members
    members = ["Ray", "Jack", "Vikran"]
    hdf5_file = 'data.h5'

    for member in members:
        # file paths
        walking_file = f'{member}Walking.csv'
        jumping_file = f'{member}Jumping.csv'

        # load and label files
        walking_df = load_and_label(walking_file, activity_label=0)
        jumping_df = load_and_label(jumping_file, activity_label=1)

        # combine dataframes
        combined_df = pd.concat([walking_df, jumping_df], ignore_index=True)

        # process combined csv and save to hdf5
        raw_data, filtered_data = preprocess_data(combined_df, hdf5_file, member)

        # plot comparison for 'accel_x'
        plot_comparison(raw_data, filtered_data, "abs_accel")
