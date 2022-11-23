# Meant to be run with `ipython -i` for exploration 

from saf_sinasc.feature_engineering import (
    load_negative_and_positive_df, 
    drop_columns, 
    pre_process_enrich_columns, 
    ensure_dtypes, 
    preprocess_inputation,
    get_dummies
)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

df1 = load_negative_and_positive_df()

df2 = drop_columns(df1)
df2 = ensure_dtypes(df2)

df = pre_process_enrich_columns(df2)
df = preprocess_inputation(df)
df = get_dummies(df)


from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
clf = DecisionTreeClassifier(random_state=0)

y = df["y"]
X = df.drop(columns=["y"])

score = cross_val_score(clf, X, y, cv=10, scoring='f1').mean()
print(score)