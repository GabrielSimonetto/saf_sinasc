"""
This module holds graphs related to model evaluation
"""
import time
import argparse

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from saf_sinasc.models import ModelEvaluator
from saf_sinasc.config import EVALUATORS_PATH, METRICS
from saf_sinasc.scripts.config import (
    MODEL_GRAPHS_OUTPUT_PATH,
    NUM_OF_FEATURES_TO_DISPLAY,
)

assert EVALUATORS_PATH.exists()


def plot_aggregated_feature_importances(
    data_version, evaluator, num_of_features_to_display=NUM_OF_FEATURES_TO_DISPLAY
):
    # TODO: get_unique_cols dinamically
    # HOLUP
    # EU NEM PRECISEI USAR SAHDIOUASHFIOASHDIOSAHFOIAHDOI

    # Take the mean of the list of feature importance per sample
    list_of_series = [
        pd.Series(fi, c)
        for fi, c in zip(evaluator.feature_importances, evaluator.training_columns)
    ]

    all_metrics = pd.DataFrame(list_of_series)

    # WHERE???
    all_metrics.to_csv("all_metrics.csv")

    fi_mean = all_metrics.mean()

    print(f"{evaluator}: ")
    print(f"fi_mean len: {len(fi_mean)}")
    print(f"evaluator.training_columns len: {len(evaluator.training_columns)}")

    # import ipdb
    # ipdb.set_trace()

    # # create a DataFrame with feature importances
    # df_importances = (
    #     pd.DataFrame(
    #         {'feature': evaluator.training_columns, 'importance': fi_mean})
    #     .sort_values('importance', ascending=False)
    #     .iloc[:num_of_features_to_display]
    # )

    df_importances = (
        fi_mean.to_frame()
        .reset_index()
        .rename(columns={"index": "feature", 0: "importance"})
        .sort_values("importance", ascending=False)
        .iloc[:num_of_features_to_display]
    )

    # plot feature importances
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="importance", y="feature", data=df_importances)
    # sns.barplot(x='Importance', y='Feature', data=feature_importance, color='b')

    save_path = (
        MODEL_GRAPHS_OUTPUT_PATH
        / data_version
        / f"{evaluator.name}_feature_importances.png"
    )

    save_path.parent.mkdir(parents=True, exist_ok=True)

    # Rotate the y-axis labels
    # ax.tick_params(axis='y', rotation=45)

    # Adjust the margins
    plt.subplots_adjust(left=0.2, right=0.8)

    plt.xlabel("Importance Score")
    plt.ylabel("Feature")
    plt.title("Feature Importance")

    plt.savefig(save_path)
    plt.clf()


def plot_from_result_metrics(data_version, evaluators, metric, agg_method):
    value_map = {
        "mean": lambda me: np.array(me.results[metric]).mean(),
        "median": lambda me: np.median(np.array(me.results[metric])),
    }

    data = {me.name: value_map[agg_method](me) for me in evaluators}

    models = list(data.keys())
    scores = list(data.values())

    title = metric.replace("_", " ").upper()
    agg_method_title = agg_method.capitalize()

    sns.set_style("whitegrid")
    plt.figure(figsize=(8, 6))
    sns.barplot(x=models, y=scores, color="b")

    plt.title(f"Model performance - {title} - {agg_method_title} ")
    plt.ylabel("Score")
    plt.xlabel("Model")

    save_path = (
        MODEL_GRAPHS_OUTPUT_PATH
        / data_version
        / f"metric_graph_{metric}_{agg_method}.png"
    )

    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path)
    plt.clf()


def create_all_model_graphs(data_version):
    start_time = time.time()

    assert EVALUATORS_PATH.joinpath(
        data_version
    ).exists(), f"Invalid data_version: {data_version}"

    evaluators = [
        ModelEvaluator.load(file)
        for file in EVALUATORS_PATH.joinpath(data_version).glob("*.joblib")
    ]

    for metric in METRICS:
        plot_from_result_metrics(data_version, evaluators, metric, "mean")
        plot_from_result_metrics(data_version, evaluators, metric, "median")

    for evaluator in evaluators:
        plot_aggregated_feature_importances(data_version, evaluator)

    end_time = time.time()

    print("Time elapsed: ", end_time - start_time, "seconds")


def validate_data_version(value):
    if not value:
        raise argparse.ArgumentTypeError("Data version cannot be an empty string.")
    return value


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create model graphs for a given data version"
    )
    parser.add_argument(
        "--data_version",
        type=validate_data_version,
        required=True,
        help="Data version number",
    )
    args = parser.parse_args()

    create_all_model_graphs(args.data_version)
