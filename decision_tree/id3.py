import pandas as pd
import numpy as np
class ID3:
    def __init__(self, max_depth=None, min_samples=10):
        # Max depth of tree and minimum samples to create another split on a node
        self.max_depth = max_depth
        self.min_samples = min_samples

    def fit(self, X, y):
        if type(X) not in ("pandas.DataFrame", "pandas.Series") or type(y) not in ("pandas.DataFrame", "pandas.Series"):
            raise TypeError("Wrong type for X or y, must be DataFrames/Series")

        features = X.columns