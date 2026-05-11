from decision_tree import id3
import numpy as np
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

tree = id3.ID3(max_depth=20, min_samples=10)    # Are these good? Who knows

df = pd.read_csv("dataset_mcts.csv")

X = df.drop("move", axis=1)
y = df["move"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=42)

tree.fit(X_train, y_train)

y_pred = tree.predict(X_test)

# 1. Check for None or missing values
none_count = sum(1 for p in y_pred if p is None)
print(f"Number of None values in y_pred: {none_count}")

# 2. Check the unique data types inside both arrays
print("y_test element types:", set(map(type, y_test)))
print("y_pred element types:", set(map(type, y_pred)))

# 3. Check the shapes
print("y_test shape:", np.shape(y_test))
print("y_pred shape:", np.shape(y_pred))

print("Accuracy: ", accuracy_score(y_test, y_pred))

joblib.dump(tree, "fitted_tree.joblib")