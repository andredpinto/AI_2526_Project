import numpy as np

def check_valid(X:np.ndarray, y:np.ndarray):
    """Makes some checks relevant for the decision tree logic"""
    assert X.ndim == 2, "X must be two dimentional"
    assert y.ndim == 1, "y must be one dimentional"
    assert X.shape[0] == y.size, "X and y must have same number of entries"


def split_dataset(col, X:np.ndarray, y:np.ndarray, split=None):
    """Col: index of column to make the split on; column is removed from resulting dataset(s)
    Split: if column split is on is numeric, split argument is required to define which value the split is made on
    RETURNS: dictionary of symbol:(X,y), for each different value to split on"""
    splits_dict = {}
    feature = X[:,col]  # Selecting feature column
    X = np.delete(X, col, axis=1)   # Removing feature column
    # !! This may cause in empty X array, which has to be handled separately

    # Will assume column is numeric if split is not None
    if split is not None:
        mask = feature < split
        if X.size != 0:
            X_left = X[mask]
            X_right = X[~mask]
        else: X_left = X_right = X  # X is empty
        splits_dict["<"] = (X_left, y[mask])
        splits_dict[">="] = (X_right, y[~mask])    # ~ is calls np.logical_not(), according to gemini, didnt check, since it worked

    else:
        uniq = np.unique(feature)
        for u in uniq:
            mask = feature == u
            if X.size != 0:
                splits_dict[u] = (X[mask], y[mask])
            else: splits_dict[u] = (X, y[mask]) # X is empty
    
    return splits_dict


def is_numeric(X:np.ndarray, col=None):
    if col is not None:
        X = X[:,col]

    unique_vals = np.unique(X)

    # checks if datatype of column derives from np.number (as do floats and ints)
    # if datatype is int and there are four or less unique values, the column is treated as categorical
    return np.issubdtype(X.dtype, np.number) and not (X.dtype.kind == "i" and unique_vals.size <= 4)


def get_majority(y:np.ndarray):
    """Returns the most frequent value in an array (1 dim)"""
    # There is probably a better way to do this
    return np.unique(y)[np.argmax(np.unique(y, return_counts=True)[1])]
    


if __name__ == "__main__":
    # These were not clanker generated, I felt like writing them myself

    categorical_X = np.array(
        [
            ["A", "D"],
            ["B", "D"],
            ["C", "E"],
            ["A", "E"],
            ["B", "F"],
            ["C", "F"]
        ]
    )
    categorical_y = np.array([1,2,3,1,2,3])

    d = split_dataset(1, categorical_X, categorical_y)
    # for k, v in d.items():
    #     print(k)
    #     print(v[0])
    #     print(v[1])
    #     print()

    #print(categorical_X)

    numerical_X = np.array(
        [
            [1,10],
            [8,1],
            [4,6],
            [100, 7],
            [-7, 8],
            [12, 70]
        ]
    )
    numerical_y = np.array([1,2,3,1,2,3])

    d = split_dataset(0, numerical_X, numerical_y, 8)
    # for k, v in d.items():
    #     print(k)
    #     print(v[0])
    #     print(v[1])
    #     print()

    y_test_maj = np.array(["a","a","b","b", "b"])
    print(get_majority(y_test_maj))