# Meant to be run with `ipython -i` for exploration 

from saf_sinasc.feature_engineering import full_pipeline
from saf_sinasc.config import SAMPLES_PATH

import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

from xgboost import XGBClassifier

from statistics import mean, median


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


def run_models(run_dt, run_rf, run_xgb):
    assert run_dt or run_rf or run_xgb, "You must choose which models will be run"

    results = {"dt": [], "rf": [], "xgb": []}

    for seed in range(5):
        sample_path = f"{SAMPLES_PATH}/5x_neutral_entries_{seed}.csv"
        df = full_pipeline(sample_path)

        y = df["y"]
        X = df.drop(columns=["y"])

        print("\n")

        if run_dt:
            score = run_dt(X, y)
            results_dt.append(score)

        if run_rf:
            score = run_rf(X, y)
            results_rf.append(score)

        if run_xgb:
            score = run_xgb(X, y)
            results_xgb.append(score)

        del df

    print(f"results_dt: {results_dt}")
    print(f"results_rf: {results_rf}")
    print(f"results_xgb: {results_xgb}")

    show_results(results_dt, "dt")
    show_results(results_rf, "rf")
    show_results(results_xgb, "xgb")

def take_metrics(clf, X, y):
    return cross_val_score(clf, X, y, cv=10, scoring='f1').mean()

def run_dt(X, y):
    clf = DecisionTreeClassifier(random_state=0)
    score = take_metrics(clf, X, y)
    print(f"run_dt score: {score}")
    return score

def run_rf(X, y):
    clf = RandomForestClassifier(random_state=0)
    score = take_metrics(clf, X, y)
    print(f"run_rf score: {score}")
    return score

def run_xgb(X, y):
    bst = XGBClassifier(random_state=0,
        n_estimators=2,
        max_depth=2,
        learning_rate=1,
        objective='binary:logistic'
    )

    score = take_metrics(bst, X, y)

    print(f"run_xgb score: {score}")
    return score

def show_results(results, model_name):
    print(f"mean {model_name}: {mean(results)}")
    print(f"median {model_name}: {median(results)}")


run_models(
    run_dt=True, run_rf=True, run_xgb=True
)
