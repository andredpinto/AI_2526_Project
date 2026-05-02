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

print("TEST FOR NUMERICAL DATASET (iris.csv)")

print("Accuracy (no catastrophic errors, it seems):", accuracy_score(y_test, y_pred))
model.print_tree()
print("=====================================================================")
# print(y_pred)
# print(pd.Series(y_pred))
# print(pd.concat([X_test, y_test], axis=1))
# print(pd.concat([X_test, pd.Series(y_pred)], axis=1))

# === Test: Fully categorical dataset ===

categorical_data = {
    "Outlook": ["sunny", "sunny", "overcast", "rainy", "rainy", "rainy", "overcast", "sunny", "sunny", "rainy", "sunny", "overcast", "overcast", "rainy"],
    "Temperature": ["hot", "hot", "hot", "mild", "cool", "cool", "cool", "mild", "cool", "mild", "mild", "mild", "hot", "mild"],
    "Humidity": ["high", "high", "high", "high", "normal", "normal", "normal", "high", "normal", "normal", "normal", "high", "normal", "high"],
    "Wind": ["weak", "strong", "weak", "weak", "weak", "strong", "strong", "weak", "weak", "weak", "strong", "strong", "weak", "strong"],
    "Play": ["no", "no", "yes", "yes", "yes", "no", "yes", "no", "yes", "yes", "yes", "yes", "yes", "no"]
}

categorical_df = pd.DataFrame(categorical_data)

X_cat = categorical_df.drop("Play", axis=1)
y_cat = categorical_df["Play"]
X_cat_train, X_cat_test, y_cat_train, y_cat_test = train_test_split(X_cat, y_cat, random_state=seed)

model_cat = ID3(min_samples=5)

model_cat.fit(X_cat_train, y_cat_train)

y_cat_pred = model_cat.predict(X_cat_test)

print("TEST FOR CATEGORICAL DATASET (small, AI generated)")
print("Categorical dataset accuracy:", accuracy_score(y_cat_test, y_cat_pred))
model_cat.print_tree()