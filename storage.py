import pandas as pd

# initialize hdfstore structure
def initialize_hdfstore():
    with pd.HDFStore("data.h5", mode='w') as store:
        members = ["ray", "jack", "vikran"]
        # initailize a minimal empty dataframe
        empty = pd.DataFrame({'Empty Column': [None]})
        # create raw data groups for each member
        for member in members:
            store.put(f'/raw/{member}', empty, format='table')
        # create pre-processed data groups for each member
        for member in members:
            store.put(f'/processed/{member}', empty, format='table')
        # create train-test split groups
        store.put('/split/train', empty, format='table')
        store.put('/split/test', empty, format='table')
    print("structure initialized.")

# print structure keys
def print_structure():
    with pd.HDFStore("data.h5", mode='r') as store:
        for key in store.keys():
            print(key)

if __name__ == "__main__":
    # initialize_hdfstore()

    # df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
    #
    # # open the HDFStore in append mode to update the key
    # with pd.HDFStore("data.h5", mode="a") as store:
    #     store.put('/raw/ray', df, format='table')
    #
    df = pd.read_hdf("data.h5", key="/raw/ray")
    print(df)

    print_structure()
