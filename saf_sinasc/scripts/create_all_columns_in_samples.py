from saf_sinasc.models import ModelEvaluator
from saf_sinasc.scripts.config import (
    MODEL_GRAPHS_OUTPUT_PATH,
    NUM_OF_FEATURES_TO_DISPLAY,
)
from saf_sinasc.config import EVALUATORS_PATH, METRICS
import glob
from saf_sinasc.config import SAMPLES_PATH
from saf_sinasc.scripts.config import SCRIPTS_OUTPUT_PATH
import pandas as pd

import time
import argparse


def evaluator_unique(evaluator, unique_columns):
    for columns in evaluator.training_columns:
        unique_columns.update(columns)

    return unique_columns


def get_unique_columns(data_version):
    start_time = time.time()
    unique_columns = set()

    assert EVALUATORS_PATH.joinpath(
        data_version
    ).exists(), f"Invalid data_version: {data_version}"

    evaluators = [
        ModelEvaluator.load(file)
        for file in EVALUATORS_PATH.joinpath(data_version).glob("*.joblib")
    ]

    for evaluator in evaluators:
        unique_columns = evaluator_unique(evaluator, unique_columns)

    end_time = time.time()
    print("Time elapsed: ", end_time - start_time, "seconds")
    return list(unique_columns)


def validate_data_version(value):
    if not value:
        raise argparse.ArgumentTypeError("Data version cannot be an empty string.")
    return value


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(
#         description='Create model graphs for a given data version')
#     parser.add_argument('--data_version', type=validate_data_version,
#                         required=True, help='Data version number')
#     args = parser.parse_args()

#     unique_columns = get_unique_columns(args.data_version)
#     # print(unique_columns)

#     with open(SCRIPTS_OUTPUT_PATH / "unique_columns.txt", 'w') as f:
#         for col in unique_columns:
#             f.write(f"{col}, \n")
