import numpy as np
from math import log

def get_enthropy(X:np.ndarray):
    # Calculates enthropy for variable X
    # It is assumed X is a numpy array?
    values, counts = np.unique(X, return_counts=True)   # Returns unique values in the array and their counts
    n = X.size
    enth = 0            # enthropy
    for i in range(values.size):
        aux = counts[i]/n
        enth -= aux*log(aux,2)
    return enth


def calculate_information_gain(X:np.ndarray, y:np.ndarray, y_enthropy=None):
    if X.size != y.size : raise ValueError("Arrays must have same size")
    if y_enthropy is None: y_enthropy = get_enthropy(y)
    n = X.size
    values, counts = np.unique(X, return_counts=True)
    for i in range(values.size):
        # Here y_enthropy is used to save memory, losing the actual y_enthropy value
        y_enthropy -= counts[i]/n*get_enthropy(y[X==values[i]])
    return y_enthropy

def check_valid(X:np.ndarray, y:np.ndarray):
    """Makes some checks relevant for the decision tree logic"""
    assert X.ndim == 2, "X must be two dimentional"
    assert y.ndim == 1, "y must be one dimentional"
    assert X.shape[0] == y.size, "X and y must have same number of entries"


if __name__=="__main__":
    # Clanker generated

    # Get enthropy tests
    arr_all_same = np.array([1, 1, 1, 1])
    assert get_enthropy(arr_all_same) == 0.0, "Test failed: homogeneous array"

    arr_binary = np.array([0, 0, 1, 1])
    assert abs(get_enthropy(arr_binary) - 1.0) < 1e-10, "Test failed: binary 50-50"

    arr_three_equal = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2])
    expected = -3 * (1/3) * np.log2(1/3)
    assert abs(get_enthropy(arr_three_equal) - expected) < 1e-10, "Test failed: three equal classes"

    arr_single = np.array([1])
    assert get_enthropy(arr_single) == 0.0, "Test failed: single element"

    # calculate_information_gain tests
    y = np.array([0, 0, 1, 1])
    X_perfect = np.array([1, 1, 2, 2])
    ig = calculate_information_gain(X_perfect, y)
    assert abs(ig - 1.0) < 1e-10, "Test failed: perfect split"

    X_no_split = np.array([1, 2, 1, 2])
    ig = calculate_information_gain(X_no_split, y)
    assert ig == 0.0, "Test failed: no correlation"

    X_binary = np.array([1, 1, 2, 2])
    y_balanced = np.array([0, 1, 0, 1])
    ig = calculate_information_gain(X_binary, y_balanced)
    assert abs(ig - 0.0) < 1e-10, "Test failed: balanced split"

    y_full = np.array([0, 0, 0, 1, 1, 1])
    X_half = np.array([1, 1, 1, 2, 2, 2])
    ig = calculate_information_gain(X_half, y_full)
    assert abs(ig - get_enthropy(y)) < 1e-10, "Test failed: perfect split 3-3"

    y_orig = np.array([0, 0, 1, 1])
    y_ent = get_enthropy(y_orig)
    ig = calculate_information_gain(X_perfect, y_orig, y_enthropy=y_ent)
    assert abs(ig - 1.0) < 1e-10, "Test failed: with precomputed entropy"
    assert y_ent == 1.0, "Test failed: y_enthropy was mutated"

    # Test that catches the weight bug - unbalanced split with partial impurities
    X_unbalanced = np.array([1, 1, 1, 2, 2])
    y_mixed = np.array([0, 0, 1, 0, 1])
    ig = calculate_information_gain(X_unbalanced, y_mixed)
    H_y = get_enthropy(y_mixed)
    H_y1 = get_enthropy(y_mixed[X_unbalanced == 1])
    H_y2 = get_enthropy(y_mixed[X_unbalanced == 2])
    expected_ig = H_y - (3/5)*H_y1 - (2/5)*H_y2
    assert abs(ig - expected_ig) < 1e-10, "Test failed: unbalanced split with impurities"

    print("All tests passed!")