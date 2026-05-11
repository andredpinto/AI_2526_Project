import joblib
import pandas as pd
from decision_tree import id3
from sklearn.metrics import accuracy_score

tree = joblib.load("fitted_tree.joblib")

df = pd.read_csv("dataset_mcts.csv")

X = df.drop("move", axis=1)
y = df["move"]

y_pred = tree.predict(X)

print("Acc: ", accuracy_score(y, y_pred))