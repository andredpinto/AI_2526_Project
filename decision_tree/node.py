import numpy as np

class DTNode:
    def __init__(self, feature_index, type="categorical"):
        # Type defines the feature type that is tested on the node (categorical or numerical)
        self.type = type
        # Pointers (?) to connected nodes
        self.parent = None
        self.left = None
        self.right = None
        # Boolean function that decides the branch to follow
        self.decision = None