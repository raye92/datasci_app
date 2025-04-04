import pandas as pd

def segment_signal(df, window=2.0):
    segments = []
    seg_id = 0
    start_time = df['time'].min()
    end_time = df['time'].max()
    current_time = start_time
    # Loop over the signal in steps of 'window' seconds
    while current_time < end_time:
        seg = df[(df['time'] >= current_time) & (df['time'] < current_time + window)]
        if not seg.empty:
            seg = seg.copy()
            seg['segment'] = seg_id  # add segment id
            segments.append(seg)
            seg_id += 1
        current_time += window
    return segments

def split():
    # load data
    a = pd.read_hdf("data.h5", key="/processed/Ray")
    b = pd.read_hdf("data.h5", key="/processed/Jack")
    c = pd.read_hdf("data.h5", key="/processed/Vikran")

    # offsetting jack, and vikran's data to not overlap
    a_end = a['time'].max()
    b['time'] = b['time'] + a_end
    b_end = b['time'].max()
    c['time'] = c['time'] + b_end

    window = 2.0  # window duration

    all_data = pd.concat([a, b, c], ignore_index=True)
    # Use the segment_signal function defined above
    segmented = segment_signal(all_data, window=window)

    # shuffle and split segments into train 90 and test 10%
    from sklearn.model_selection import train_test_split
    train_segments, test_segments = train_test_split(
        segmented, test_size=0.10, random_state=42, shuffle=True
    )

    # concatenate DataFrames and store in hdf5
    train_df = pd.concat(train_segments, ignore_index=True)
    test_df = pd.concat(test_segments, ignore_index=True)
    with pd.HDFStore("data.h5") as store:
        store.put('/split/train', train_df, format='table')
        store.put('/split/test', test_df, format='table')

    print("Training and test splits stored successfully.")

def print_structure():
    with pd.HDFStore("data.h5", mode='r') as store:
        for key in store.keys():
            print(key)

if __name__ == "__main__":
    # initialize_hdfstore()  # if needed
    split()
    print_structure()
