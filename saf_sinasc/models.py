
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

class Model:
    def __init__(self, name, model):
        self.name = name
        self.model = model
        self.results = []

    def run(self, X, y):
        score = self.take_metrics(X, y)
        print(f"{self.name} score: {score}")
        self.results.append(score)

    def show_results(self):
        print(f"{self.name} results: {self.results}\n")

    def take_metrics(self, X, y):
        return cross_val_score(self.model, X, y, cv=10, scoring='f1').mean()

    def aggregate_results(self):
        print(f"mean {self.name}: {mean(self.results)}")
        print(f"median {self.name}: {median(self.results)}\n")


def default_run_models():
    dt = Model("DT", DecisionTreeClassifier(random_state=0))
    rf = Model("RF", RandomForestClassifier(random_state=0))
    xgb = Model("XGB", XGBClassifier(random_state=0,
                                     n_estimators=2,
                                     max_depth=2,
                                     learning_rate=1,
                                     objective='binary:logistic'
                                     ))

    return run_models(
        [dt, rf, xgb]
    )


def run_models(models):
    assert len(models) != 0, "You must insert which models will be run"

    # TODO: ask range to user
    for seed in range(5):
        sample_path = f"{SAMPLES_PATH}/5x_neutral_entries_{seed}.csv"
        df = full_pipeline(sample_path)

        y = df["y"]
        X = df.drop(columns=["y"])

        for model in models:
            model.run(X, y)

        print("\n")

        del df

    for model in models:
        model.show_results()

    for model in models:
        model.aggregate_results()
