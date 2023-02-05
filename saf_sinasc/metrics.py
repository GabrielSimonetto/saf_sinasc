from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
clf = DecisionTreeClassifier(random_state=0)

def get_metrics(df):
    y = df["y"]
    X = df.drop(columns=["y"])

    return cross_val_score(clf, X, y, cv=10, scoring='f1').mean()
    