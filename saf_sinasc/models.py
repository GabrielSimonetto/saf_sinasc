
from statistics import mean, median
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from saf_sinasc.feature_engineering import full_pipeline
from saf_sinasc.config import SAMPLES_PATH

import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


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


def default_run_models():
    dt = DecisionTreeClassifier(random_state=0)

    rf = RandomForestClassifier(random_state=0)

    bst = XGBClassifier(random_state=0,
                        n_estimators=2,
                        max_depth=2,
                        learning_rate=1,
                        objective='binary:logistic'
                        )

    return run_models(
        [("dt", dt), ("rf", rf), ("bst", bst)]
    )


def run_models(model_list):
    assert len(model_list) != 0, "You must insert which models will be run"

    results = {model_name: [] for model_name, _ in model_list}

    # TODO: ask range to user
    for seed in range(5):
        sample_path = f"{SAMPLES_PATH}/5x_neutral_entries_{seed}.csv"
        df = full_pipeline(sample_path)

        y = df["y"]
        X = df.drop(columns=["y"])

        print("\n")

        for model_name, model in model_list:
            score = take_metrics(model, X, y)
            print(f"run_{model_name} score: {score}")
            results[model_name].append(score)

        print("\n")
        del df

    for name, metric_values in results.items():
        print(f"results {name}: {metric_values}")

    for name, metric_values in results.items():
        show_results(name, metric_values)


def take_metrics(clf, X, y):
    return cross_val_score(clf, X, y, cv=10, scoring='f1').mean()


def run_decision_tree(X, y):
    clf = DecisionTreeClassifier(random_state=0)
    score = take_metrics(clf, X, y)
    print(f"run_dt score: {score}")
    return score


def run_random_forest(X, y):
    clf = RandomForestClassifier(random_state=0)
    score = take_metrics(clf, X, y)
    print(f"run_rf score: {score}")
    return score


def run_xgboost(X, y):
    bst = XGBClassifier(random_state=0,
                        n_estimators=2,
                        max_depth=2,
                        learning_rate=1,
                        objective='binary:logistic'
                        )

    score = take_metrics(bst, X, y)

    print(f"run_xgb score: {score}")
    return score

# TODO: metrics per model func + aggregating metrics func


def show_results(model_name, results):
    print(f"mean {model_name}: {mean(results)}")
    print(f"median {model_name}: {median(results)}")


# run_models(
#     run_dt=True, run_rf=True, run_xgb=True
# )
