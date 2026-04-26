import numpy as np

class DTNode:
    def __init__(self, feature_index=None, children:dict=None, parent=None, enthropy=None, numerical=False, split=None, value=None):
        """Feature index - index of the feature on the original dataset (collumn name)
        Children - dictionary with split values and corresponding node, like {'Yes':Node, 'No':Node}
        Parent - parent node
        Enthropy - enthropy value on current node, not sure if it will be used, more for display reasons
        Numerical - true if node is associated with a numeric feature; if so split argument must exist
        Split - determines the value where split is made on numerical features
        Value - only for leaf nodes, defines the value of the target value returned by the tree"""
        self.feature_index = feature_index 
        self.children = children if children is not None else {}
        self.parent = parent
        self.enthropy = enthropy
        self.numerical = numerical
        self.value = value
        if self.numerical: self.split = split

    # AI-generated getters and setters
    def get_feature(self):
        return self.feature_index

    def set_feature(self, feature_index):
        self.feature_index = feature_index
        return self

    def get_children(self):
        return self.children

    def get_child(self, value):
        return self.children.get(value)

    def add_child(self, value, node, auto_parent=True):
        self.children[value] = node
        if auto_parent:
            node.parent = self
        return self

    def remove_child(self, value):
        if value in self.children:
            del self.children[value]
        return self

    def get_parent(self):
        return self.parent

    def set_parent(self, node):
        self.parent = node
        return self

    def get_entropy(self):
        return self.enthropy

    def set_entropy(self, enthropy):
        self.enthropy = enthropy
        return self

    def is_numerical(self):
        return self.numerical

    def set_numerical(self, numerical):
        self.numerical = numerical
        return self

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
        return self

    def is_leaf(self):
        return self.value is not None

    def num_children(self):
        return len(self.children)

    def has_child(self, value):
        return value in self.children

    # This one was made by me 
    def get_next(self, X):
        """Receives an entry as a 1-dim numpy array, and moves forward on the tree based on its features
        Returns next node, corresponding to the right path
        If used on child node raises error"""
        if self.is_leaf(): raise ValueError("Node is leaf, has no children; check node.is_leaf() before calling this method")
        val = X[self.feature_index]
        if val not in self.children:
            raise ValueError(f'Value "{val}" not found in node children')
        return self.get_child(val)