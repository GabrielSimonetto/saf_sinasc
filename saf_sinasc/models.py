
from statistics import mean, median, stdev
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score, cross_validate
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from saf_sinasc.feature_engineering import full_pipeline
from saf_sinasc.config import SAMPLES_PATH, METRICS

import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


# TODO: remove ghosts, insert in a .env and make .sh and .py files use it.
# output_path="data/compilations/samples/5x_neutral_entries_$seed.csv";

# TODO: just glob it? I think i wanna have control over which one is being iterated on.
# TODO: I can use "seed" here for congruency, but here it is just a version (seed_version? version_seed?)
# sample_paths = [f"data/compilations/samples/5x_neutral_entries_{seed}.csv" for seed in range(5)]

class ModelEvaluator:
    def __init__(self, name, model):
        self.name = name
        self.model = model
        self.results = {metric: [] for metric in METRICS}
        self.training_columns = []
        self.feature_importances = []

    def __str__(self):
        return f"ModelEvaluator({self.name})"

    def __repr__(self):
        return f"ModelEvaluator({self.name})"

    def run(self, X, y):
        scores = self.take_metrics(X, y)
        # TODO use logging instead of print in order to configure verbosity
        # print(f"{self.name} scores: {score:.2f}")

        for metric in METRICS:
            self.results[metric].append(scores[metric])

        # TODO: this should be checked later if it is the best approach for getting a fitted model
        #   right now, sine take_   metrics only uses cross validation
        #   we don't have access to a fitted model in order to get feature_importances,
        #   so, this is costly and probably there's a better way to get a fitted model out of the CV process

        # TODO: also, there is no guarantee that every model works with a feature_importances basis
        #   this should be somewhat checked or at least asserted.
        self.training_columns = X.columns
        self.model.fit(X, y)
        self.feature_importances.append(self.model.feature_importances_)

    def show_results(self):
        # TODO: precision formatting should be handled only once, instead of take_metrics everywhere
        # either on input, either as a class that knows how to print itself already formatted.

        print("Results:")
        for metric in METRICS:
            print(
                f"{self.name:>4} {metric:>8}: {[ '%.2f' % num for num in self.results[metric] ]}".ljust(50))
        print()

    def take_metrics(self, X, y, metrics=METRICS):
        # sklearn.metrics.roc_auc_score(y_true, y_score)
        # return cross_val_score(self.model, X, y, cv=10, scoring='f1').mean()

        assert len(METRICS) > 1, "Needs functionality for only one metric"
        # TODO: if > 2 metrics, cross_validate produces test_{metric} names
        #       if ==1 ; it simplifies to test_score, which breaks the current code.

        cv_results = cross_validate(self.model, X, y, cv=10, scoring=metrics)

        return {k.lstrip('test_'): v.mean() for k, v in cv_results.items() if k.startswith('test_')}

    def aggregate_results(self):
        print()
        for metric in METRICS:
            print(
                f"{self.name:>4} {metric:>8}   mean: {mean(self.results[metric]):.2f}".ljust(50))
            print(
                f"{self.name:>4} {metric:>8} median: {median(self.results[metric]):.2f}".ljust(50))

            if len(self.results[metric]) > 1:
                print(
                    f"{self.name:>4} {metric:>8}  stdev: {stdev(self.results[metric]):.2f}".ljust(50))


def default_run_models(num_samples=5):
    dt = ModelEvaluator("DT", DecisionTreeClassifier(random_state=0))
    rf = ModelEvaluator("RF", RandomForestClassifier(random_state=0))
    xgb = ModelEvaluator("XGB", XGBClassifier(random_state=0,
                                              n_estimators=2,
                                              max_depth=2,
                                              learning_rate=1,
                                              objective='binary:logistic'
                                              ))

    return run_models(
        [dt, rf, xgb], num_samples
    )


def run_models(models, num_samples=5):
    assert len(models) != 0, "You must insert which models will be run"

    # TODO: ask range to user
    for seed in range(num_samples):
        print(f"running seed {seed}")

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

    # Will hold only the last model, but all the metrics.
    return models
