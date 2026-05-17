import pandas as pd
import numpy as np
from decision_tree.metrics import *
from decision_tree.auxiliar import *
from decision_tree.node import *
import random

class ID3:
    def __init__(self, max_depth=None, min_samples=10):
        # Max depth of tree and minimum samples to create another split on a node
        self.max_depth = max_depth
        self.min_samples = min_samples
        self.root = None

    # TREE TRAINING
    def fit(self, X, y):
        if isinstance(X, pd.DataFrame):
            self.features = X.columns   # Used to print the tree
            X = X.values    # .values returns a numpy representation of the dataframe, probably withouth the feature names
        if isinstance(y, pd.Series):
            y = np.array(y.values)
        self.target_type = y.dtype

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
                for split in possible_splits:
                    mask = col <= split     # Transforms numeric collumn into something like [True, False, False, ...]
                    # From here, same as categorical
                    ig = calculate_information_gain(mask, y, enth_y)
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
    

    def _build_tree(self, X:np.ndarray, y:np.ndarray, depth):
        """Builds the decision tree recursively"""

        # Return node
        node = DTNode()

        # Stopping conditions (returned node is a leaf)
        if X.size == 0 or (self.max_depth is not None and depth > self.max_depth) or y.size < self.min_samples or get_enthropy(y)==0:
            node.set_value(get_majority(y))
            return node
        
        # If not, continue building tree
        split_col, numeric_split = self._get_best_split(X, y)
        node.set_feature(split_col)
        node.set_majority(get_majority(y))
        if numeric_split is not None:
            node.set_numerical(True, numeric_split)
        for child_val, data_splits in split_dataset(split_col, X, y, numeric_split).items():
            node.add_child(child_val, self._build_tree(data_splits[0], data_splits[1], depth+1))
        return node
    # =======================================================

    # PREDICTING
    def predict(self, X):
        if self.root is None: raise RuntimeError("Maybe try fitting the model first? (you dumb bitch)")
        if isinstance(X, pd.DataFrame):
            X = X.values    # .values returns a numpy representation of the dataframe, probably withouth the feature names

        assert isinstance(X, np.ndarray), "X isnt np.ndarray, check yo code"

        # Here it is assumed that prediction variable is a string
        #TODO: add case for int values, for the game
        if self.target_type.kind == "i":
            y_pred = np.empty(X.shape[0], dtype=np.int64) # if when using objects to represent ints weird things were happening when trying to measure accuracy
        else:
            y_pred = np.empty(X.shape[0], dtype=object) # setting the data type as object makes it so the strings lenth is variable

        for entry in range(y_pred.size):
            y_pred[entry] = self._make_prediction(X[entry], self.root)
        
        return y_pred

    #this will do the prediction, going to a leaf node
    #the nodes only save the majority class, so what i'm thinking
    #is if the majority class is in the valid_moves then ok
    #if not go to their parents
    #and if no parent has a valid_move as the majority
    #just return a random valid move
    #this assumes X is just one board
    def predict_valid(self, X, valid_moves:list, verbose=False):
        """if verbose=True -> prints something saying it choose a random valid move"""
        if self.root is None: raise RuntimeError("Maybe try fitting the model first? (you dumb bitch)")
        if isinstance(X, pd.DataFrame):
            X = X.values    # .values returns a numpy representation of the dataframe, probably withouth the feature names
        assert isinstance(X, np.ndarray), "X isnt np.ndarray, check yo code"

        node = self._get_leaf(X, self.root)

        #while we dont run out of nodes
        while node is not None:
            if node.get_value() is not None:
                pred = node.get_value()
            else:
                pred = node.get_majority()
            if pred in valid_moves:
                return pred
            node = node.get_parent()

        if verbose:
            print("random choice has to be made")
        return random.choice(valid_moves)

    #copy paste of _make_prediction without the numerical bs
    #assumes categorical data, like the pieces in our board
    def _get_leaf(self, x:np.ndarray, node:DTNode):
        if node.get_value() is not None: return node

        assert x.ndim == 1, "One entry at a time, please"

        val = x[node.get_feature()]
        x = np.delete(x, node.get_feature())
        if val not in node.get_children(): 
            #raise NotImplementedError("Must figue out a way to deal with missing values, maybe keep max class in the node")
            return node
        else:
            return self._get_leaf(x, node.get_children()[val])

    def _make_prediction(self, x:np.ndarray, node:DTNode):
        if node.get_value() is not None: return node.get_value()

        assert x.ndim == 1, "One entry at a time, please"

        val = x[node.get_feature()]
        if node.is_numerical():
            if val < node.get_split(): val = "<"
            else: val = ">="
        x = np.delete(x, node.get_feature())
        if val not in node.get_children(): 
            #raise NotImplementedError("Must figue out a way to deal with missing values, maybe keep max class in the node")
            return node.get_majority()
        else:
            return self._make_prediction(x, node.get_children()[val])

    def print_tree(self):
        """
        Recursively prints the decision tree in the console.
        Call this without arguments after fitting: my_model.print_tree()
        """
        # Initialize at the root if no node is passed
        if self.root is None:
            print("The tree is empty. Please fit the model first.")
            return
            
        self._print_tree(self.root, 0, "Root", np.zeros(self.features.size, dtype=np.int8))

        
    def _print_tree(self, node:DTNode, depth, rule, offsets:np.ndarray):
        # AI GENERATED, I DIDNT CHECK THE CODE
        # Formatting: creating indentation based on the depth of the tree
        indent = "    " * depth

        # BASE CASE: It's a leaf node
        if node.get_value() is not None:
            print(f"{indent}└─ {rule}  --->  Predict: {node.get_value()}")
            return

        # RECURSIVE STEP: It's a decision node
        feature_index= node.get_feature()
        feature = self.features[feature_index + offsets[feature_index]]
        offsets[feature_index:] += 1    # Every feature right of node feature is shifted left (-1)
        print(f"{indent}└─ {rule}  --->  [Split: Feature {feature}]")

        # Iterate through the children and print them
        for key, child in node.get_children().items():
            
            # Format the rule depending on if it was a numeric or categorical split
            if getattr(node, 'is_numerical', False) and node.is_numerical():
                # For numeric splits, the key is typically a boolean (True for <= split, False for > split)
                split_val = node.get_split()
                if key == "<":
                    child_rule = f"If Feature {feature} < {split_val:.2f}"
                else:
                    child_rule = f"If Feature {feature} >= {split_val:.2f}"
            else:
                # For categorical splits, the key is the exact feature value
                child_rule = f"If Feature {feature} == '{key}'"
            
            # Recurse down to the child
            self._print_tree(child, depth + 1, child_rule, offsets.copy())


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