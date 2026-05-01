import pandas as pd
from id3 import ID3
from pathlib import PurePath
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

seed = 69

df = pd.read_csv(PurePath("..", "data", "iris.csv"), index_col="ID")

X = df.drop("class", axis=1)
y = df["class"]
X_train, X_test, y_train, y_test= train_test_split(X, y, random_state=seed)

model = ID3()

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy (no catastrophic errors, it seems):", accuracy_score(y_test, y_pred))
# print(y_pred)
# print(pd.Series(y_pred))
# print(pd.concat([X_test, y_test], axis=1))
# print(pd.concat([X_test, pd.Series(y_pred)], axis=1))