import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from decision_tree import id3
import numpy as np
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from pathlib import PurePath, Path

# IMPORTANT: DUE TO THE ABSOLUTE PATHS USED, THIS FILE MUST BE RUN FROM THE PROJECT'S ROOT DIRECTORY

data_path = PurePath("data",  "dataset_mcts.csv")
df = pd.read_csv(data_path)

X = df.drop("move", axis=1)
y = df["move"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

max_d_list = [None, 5, 10, 50, 100]
min_s_list = [1,2,5,10,20,50]
save_location = Path("decision_tree", "pre_trained_trees")

for max_d in max_d_list:
    for min_s in min_s_list:
        tree = id3.ID3(max_depth=max_d, min_samples=min_s)
        tree.fit(X_train, y_train)
        tree_name = f"tree{max_d}_{min_s}.joblib"
        joblib.dump(tree, Path(save_location, tree_name))
        y_pred = tree.predict(X_test)

        print(f"Accuracy (max_depth:{max_d}, min_samples:{min_s}): ", accuracy_score(y_test, y_pred))

print("Done")
