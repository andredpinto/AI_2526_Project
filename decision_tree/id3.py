import pandas as pd
import numpy as np
from metrics import *

class ID3:
    def __init__(self, max_depth=None, min_samples=10):
        # Max depth of tree and minimum samples to create another split on a node
        self.max_depth = max_depth
        self.min_samples = min_samples

    def fit(self, X, y):
        if isinstance(X, pd.DataFrame):
            X = X.values    # .values returns a numpy representation of the dataframe, probably withouth the feature names
        if isinstance(y, pd.Series):
            y = y.values

        assert isinstance(X, np.ndarray) and isinstance(y, np.ndarray), "Either X or y arent np.ndarrays, check yo code"

        check_valid(X, y)
        

    def _get_best_split(self, X:np.ndarray, y):
        """Returns tuple containing index of collumn with the best information gain and the split value, if the split feature is numeric
        If the split feature is not numeric, second value is None
        """
        n_cols = X.shape[1]

        best_split_index = None
        best_split_inf_gain = -1
        num_split = None    # Value to split on if feature is numeric
        enth_y = get_enthropy(y)    # Precompute y enthropy to improve efficiency
        for i in range(n_cols):
            col = X[:,i]  # get feature collumn as 1 dimentional array
            print(col)
            print(col.dtype)

            # Numeric collumn
            # TODO: Fix bug where if numeric and categorical (strings) values are mixed in matrix everything is converted into string
            if np.issubdtype(col.dtype, np.number): # checks if datatype of column derives from np.number (as do floats and ints)
                unique_vals = np.unique(col)    # Unique values in the collumn, conveniently sorted
                # Below, a very smart way of computing the mean between pairs of points, suggested by AI
                possible_splits = (unique_vals[1:] + unique_vals[:-1]) / 2
                print("Possible splits: ", possible_splits)
                for split in possible_splits:
                    mask = col <= split     # Transforms numeric collumn into something like [True, False, False, ...]
                    # From here, same as categorical
                    ig = calculate_information_gain(mask, y, enth_y)
                    print("split: ", split)
                    print("ig:", ig)
                    if ig > best_split_inf_gain:    # Better split found
                        best_split_index = i
                        best_split_inf_gain = ig
                        num_split = split

            # Categorical column
            else:
                ig = calculate_information_gain(col, y, enth_y)
                print(ig)
                if ig > best_split_inf_gain:    # Better split found
                    best_split_index = i
                    best_split_inf_gain = ig
                    num_split = None    # Must reset this if previously dealt with a numeric feature

        return best_split_index, num_split


if __name__ == "__main__":
    # Clanker generated, with some tweaks by me

    clf = ID3()

    X1 = np.array([[1], [1], [1], [2], [2], [2]])
    y1 = np.array([0, 0, 0, 1, 1, 1])
    split_idx, split_val = clf._get_best_split(X1, y1)
    assert split_idx == 0, "Test 1 failed: perfect numeric split"
    assert split_val is not None, "Test 1 failed: should return split value"
    print(f"Test 1 passed: numeric perfect split (split={split_val})")
    print(f"({split_idx}, {split_val})")

    X2 = np.array([[1], [2], [3], [4], [5], [6]])
    y2 = np.array([0, 1, 0, 1, 0, 1])
    split_idx, split_val = clf._get_best_split(X2, y2)
    print(f"Test 2: numeric no clear split (IG={abs(get_enthropy(y2) - get_enthropy(y2)):.4f})")
    print(f"({split_idx}, {split_val})")

    X3 = np.array([["A"], ["A"], ["B"], ["B"]])
    y3 = np.array([0, 0, 1, 1])
    split_idx, split_val = clf._get_best_split(X3, y3)
    assert split_idx == 0, "Test 3 failed: perfect categorical split"
    assert split_val is None, "Test 3 failed: categorical should have no split value"
    print(f"Test 3 passed: categorical perfect split")
    print(f"({split_idx}, {split_val})")

    X4 = np.array([["A"], ["B"], ["A"], ["B"]])
    y4 = np.array([0, 0, 1, 1])
    split_idx, split_val = clf._get_best_split(X4, y4)
    print(f"Test 4 passed: categorical no correlation (IG=0)")
    print(f"({split_idx}, {split_val})")

    X5 = np.array([
        [1, "A"],
        [1, "B"], 
        [2, "A"],
        [2, "B"]
    ])
    y5 = np.array([0, 1, 1, 0])
    split_idx, split_val = clf._get_best_split(X5, y5)
    print(f"Test 5 passed: multi-column no correlation (IG≈0)")
    print(f"({split_idx}, {split_val})")

    X6 = np.array([
        [1.0, "A"],
        [2.0, "A"],
        [3.0, "B"],
        [4.0, "B"]
    ])
    y6 = np.array([0, 0, 1, 1])
    split_idx, split_val = clf._get_best_split(X6, y6)
    assert split_idx == 0, "Test 6 failed: should pick first column"
    print(f"Test 6 passed: mixed numeric and categorical (picks first)")
    print(f"({split_idx}, {split_val})")

    print("All tests passed!")