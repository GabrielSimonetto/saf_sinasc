# Meant to be run with `ipython -i` for exploration 

from saf_sinasc.feature_engineering import full_pipeline

import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

df = full_pipeline()


from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
clf = DecisionTreeClassifier(random_state=0)

y = df["y"]
X = df.drop(columns=["y"])

score = cross_val_score(clf, X, y, cv=10, scoring='f1').mean()
print(score)