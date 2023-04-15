"""
This module holds graphs related to model evaluation
"""
import time

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from saf_sinasc.models import ModelEvaluator
from saf_sinasc.config import EVALUATORS_PATH
from saf_sinasc.scripts.config import MODEL_GRAPHS_OUTPUT_PATH, NUM_OF_FEATURES_TO_DISPLAY

assert EVALUATORS_PATH.exists()


def plot_aggregated_feature_importances(evaluator, num_of_features_to_display=NUM_OF_FEATURES_TO_DISPLAY):
    # Take the mean of the list of feature importance per sample
    fi_mean = pd.DataFrame(evaluator.feature_importances).mean()

    # create a DataFrame with feature importances
    df_importances = (
        pd.DataFrame(
            {'feature': evaluator.training_columns, 'importance': fi_mean})
        .sort_values('importance', ascending=False)
        .iloc[:num_of_features_to_display]
    )

    # plot feature importances
    sns.barplot(x='importance', y='feature', data=df_importances)

    save_path = MODEL_GRAPHS_OUTPUT_PATH / \
        DATA_VERSION / f"{evaluator.name}.png"

    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path)


def create_all_model_graphs(data_version):
    start_time = time.time()

    assert EVALUATORS_PATH.joinpath(
        data_version).exists(), f"Invalid data_version: {data_version}"

    evaluators = [ModelEvaluator.load(file) for file in EVALUATORS_PATH.joinpath(
        data_version).glob("*.joblib")]

    for evaluator in evaluators:
        plot_aggregated_feature_importances(evaluator)

    end_time = time.time()

    print("Time elapsed: ", end_time - start_time, "seconds")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Create model graphs for a given data version')
    parser.add_argument('--data_version', type=str,
                        required=True, help='Data version number')
    args = parser.parse_args()

    create_all_model_graphs(args.data_version)
