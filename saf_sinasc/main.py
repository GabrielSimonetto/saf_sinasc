# Meant to be run with `ipython -i` for exploration 

from saf_sinasc.feature_engineering import full_pipeline
from saf_sinasc.config import SAMPLES_PATH

import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score


# TODO: remove ghosts, insert in a .env and make .sh and .py files use it.
# output_path="data/compilations/samples/5x_neutral_entries_$seed.csv";

# TODO: just glob it? I think i wanna have control over which one is being iterated on.
# TODO: I can use "seed" here for congruency, but here it is just a version (seed_version? version_seed?)
# sample_paths = [f"data/compilations/samples/5x_neutral_entries_{seed}.csv" for seed in range(5)] 

# TODO: maybe allows for coprehensions, 
#        but I still need to load and transform
#        don't know if I want another full_process_AGAIN()
# results = [full_process_AGAIN(i) for i in range(5)]
# def train():
# def test():
# def train_test():

results = []
for seed in range(5):
    sample_path = f"{SAMPLES_PATH}/5x_neutral_entries_{seed}.csv"  
    df = full_pipeline(sample_path)

    clf = DecisionTreeClassifier(random_state=0)

    y = df["y"]
    X = df.drop(columns=["y"])

    score = cross_val_score(clf, X, y, cv=10, scoring='f1').mean()
    print(score, "\n")

    results.append(score)

print(f"results: {results}")

from statistics import mean, median 

print(f"mean: {mean(results)}")
print(f"median: {median(results)}")

