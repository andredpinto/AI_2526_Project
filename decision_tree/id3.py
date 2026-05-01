import pandas as pd
import numpy as np
from metrics import *
from auxiliar import *
from node import *

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

        self.root = self._build_tree(X, y, 0)
        

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
            unique_vals = np.unique(col)    # Unique values in the collumn, conveniently sorted

            # Numeric collumn
            # TODO: Fix bug where if numeric and categorical (strings) values are mixed in matrix everything is converted into string
            # Update on this TODO: I dont care; both of our datasets only have one data type, so this wont pose a problem for us
            # Please remember for the future that this algorithm cant handle datasets with mixed data types
            if is_numeric(col): 
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
                #print(ig)
                if ig > best_split_inf_gain:    # Better split found
                    best_split_index = i
                    best_split_inf_gain = ig
                    num_split = None    # Must reset this if previously dealt with a numeric feature

        return best_split_index, num_split
    

    def _build_tree(X:np.ndarray, y:np.ndarray, depth):
        """Builds the decision tree recursively"""

        # Return node
        node = DTNode()
        # Stopping conditions (returned node is a leaf)
        


if __name__ == "__main__":
    clf = ID3()

    # Test 1: float arrays (treated as numeric)
    X1 = np.array([[1.0], [1.0], [1.0], [2.0], [2.0], [2.0]])
    y1 = np.array([0, 0, 0, 1, 1, 1])
    split_idx, split_val = clf._get_best_split(X1, y1)
    assert split_idx == 0, "Test 1 failed: perfect numeric split"
    assert split_val is not None, "Test 1 failed: should return split value"
    print(f"Test 1 passed: float array numeric (split={split_val})")

    # Test 2: float arrays no clear split
    X2 = np.array([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]])
    y2 = np.array([0, 1, 0, 1, 0, 1])
    split_idx, split_val = clf._get_best_split(X2, y2)
    print(f"Test 2 passed: float array no clear split")

    # Test 3: int arrays with more than 4 unique values (treated as numeric)
    X3 = np.array([[1], [2], [3], [4], [5], [6], [7], [8]])
    y3 = np.array([0, 0, 1, 1, 0, 0, 1, 1])
    split_idx, split_val = clf._get_best_split(X3, y3)
    assert split_idx == 0, "Test 3 failed: should pick column"
    assert split_val is not None, "Test 3 failed: should return split value for numeric"
    print(f"Test 3 passed: int array >4 unique values numeric (split={split_val})")

    # Test 4: int arrays with exactly 4 unique values (treated as categorical)
    X4 = np.array([[1], [2], [3], [4], [1], [2], [3], [4]])
    y4 = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    split_idx, split_val = clf._get_best_split(X4, y4)
    assert split_idx == 0, "Test 4 failed: should pick column"
    assert split_val is None, "Test 4 failed: categorical should have no split value"
    print(f"Test 4 passed: int array 4 unique values categorical")

    # Test 5: int arrays with 3 unique values (treated as categorical)
    X5 = np.array([[1], [2], [3], [1], [2], [3]])
    y5 = np.array([0, 0, 1, 1, 0, 1])
    split_idx, split_val = clf._get_best_split(X5, y5)
    assert split_idx == 0, "Test 5 failed: should pick column"
    assert split_val is None, "Test 5 failed: categorical should have no split value"
    print(f"Test 5 passed: int array 3 unique values categorical")

    print("All tests passed!")