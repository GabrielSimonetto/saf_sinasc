import os
from saf_sinasc.config import SAMPLES_PATH, METRICS, EVALUATORS_PATH, SEEDS_FILE
from saf_sinasc.feature_engineering import full_pipeline
from joblib import dump, load
from statistics import mean, median, stdev
from xgboost import XGBClassifier
from sklearn.model_selection import cross_validate
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

import pandas as pd

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)


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
        for metric in METRICS:
            self.results[metric].append(scores[metric])

        self.training_columns.append(X.columns)
        self.model.fit(X, y)
        self.feature_importances.append(self.model.feature_importances_)

        print(f"self.training_columns len = {len(X.columns)}")
        print(
            f"self.model.feature_importances_ len = {len(self.model.feature_importances_)}"
        )

    def print_all(self):
        print(f"self.name = {self.name}")
        print(f"self.model = {self.model}")
        print(f"self.results = {self.results}")
        print(f"self.training_columns = {self.training_columns}")
        print(f"self.feature_importances = {self.feature_importances}")

    def show_results(self):
        # TODO: precision formatting should be handled only once, instead of take_metrics everywhere
        # either on input, either as a class that knows how to print itself already formatted.

        print("Results:")
        for metric in METRICS:
            print(
                f"{self.name:>4} {metric:>8}: {[ '%.2f' % num for num in self.results[metric] ]}".ljust(
                    50
                )
            )
        print()

    def take_metrics(self, X, y, metrics=METRICS):
        # The patterns of naming change if only one metric is present
        # assert len(METRICS) > 1, "Functionality for only one metric not implemented"
        cv_results = cross_validate(self.model, X, y, cv=10, scoring=metrics)
        return {
            k.lstrip("test_"): v.mean()
            for k, v in cv_results.items()
            if k.startswith("test_")
        }

    def get_agg(self, metric, agg):
        if agg == "mean":
            return f"{mean(self.results[metric]): .2f}"
        elif agg == "median":
            return f"{median(self.results[metric]): .2f}"
        elif agg == "stdev":
            return f"{stdev(self.results[metric]): .2f}"
        else:
            raise Exception(f"invalid agg: {agg}")

    def aggregate_results(self):
        print()
        for metric in METRICS:
            print(
                f"{self.name:>4} {metric:>8}   mean: {mean(self.results[metric]):.2f}".ljust(
                    50
                )
            )
            print(
                f"{self.name:>4} {metric:>8} median: {median(self.results[metric]):.2f}".ljust(
                    50
                )
            )

            if len(self.results[metric]) > 1:
                print(
                    f"{self.name:>4} {metric:>8}  stdev: {stdev(self.results[metric]):.2f}".ljust(
                        50
                    )
                )

    def save(self, data_version_path):
        path = (
            EVALUATORS_PATH / data_version_path / f"model_evaluator_{self.name}.joblib"
        )

        path.parent.mkdir(parents=True, exist_ok=True)
        dump(self, path)

    def load(file):
        return load(file)


def default_run_models(num_samples=5, save=False, use_seeds_file=False):
    """
    Args:
        num_samples (int, optional): Used to find sequential samples, only used if use_seeds_file=False. Defaults to 5.
        save (bool, optional): Saves Evaluators after running. Defaults to False.
        use_seeds_file_file (bool, optional): Used to use a list of seeds as sample name. Defaults to False.

    Returns: Evaluators list
    """
    dt = ModelEvaluator("DT", DecisionTreeClassifier(random_state=0))
    rf = ModelEvaluator("RF", RandomForestClassifier(random_state=0))
    xgb = ModelEvaluator(
        "XGB",
        XGBClassifier(
            random_state=0,
            n_estimators=2,
            max_depth=2,
            learning_rate=1,
            objective="binary:logistic",
        ),
    )

    evaluators = run_models([dt, rf, xgb], num_samples, use_seeds_file)

    # TODO: ah eh eu ia permitir data_version
    # #         como command line ali do lado de fora
    if save:
        save_model_evaluators(evaluators)

    return evaluators


def save_model_evaluators(model_evaluators, data_version=None):
    """Saves all model_evaluators inside `{EVALUATORS_PATH}/{data_version_path}/{name for name in model_names}.joblib`

    `data_version_path` intends to retain sequentiality between data versions,
    besides using suffix 0 for user inputted names, and 1 for versions without a name assigned to them
    """

    suffix = "0" if data_version else "1"

    num_files = len(
        [file for file in os.listdir(EVALUATORS_PATH) if file.startswith(suffix)]
    )
    data_version_path = f"{suffix}{num_files:03d}_{data_version}".strip("_None")

    for evaluator in model_evaluators:
        evaluator.save(data_version_path)


def get_seeds_from_file(file_path):
    with open(file_path, "r") as file:
        for line in file:
            yield line.strip()


def run_models(models, num_samples, use_seeds_file):
    assert len(models) != 0, "You must insert which models will be run"

    seed_iterator = (
        get_seeds_from_file(SEEDS_FILE) if use_seeds_file else range(num_samples)
    )

    for seed in seed_iterator:
        if seed == "":
            continue

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
