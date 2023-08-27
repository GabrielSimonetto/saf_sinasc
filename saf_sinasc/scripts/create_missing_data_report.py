"""
Just creates how much missing data we have on the sample
"""

import missingno as msno
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import json
import time
import subprocess
import tempfile


from glob import glob
from pathlib import Path

import missingno as msno

from saf_sinasc.feature_engineering import load_negative_and_positive_df
from saf_sinasc.scripts.config import COMPILATIONS_PATH, SCRIPTS_OUTPUT_PATH

start_time = time.time()

PERCENTAGE = "2"
# TODO: bad name, should reflect not having positive entries
NEGATIVES_PATH = SCRIPTS_OUTPUT_PATH / \
    f"eda_sample_stratified_on_{PERCENTAGE}_percentage.csv"

assert SCRIPTS_OUTPUT_PATH.exists()
assert COMPILATIONS_PATH.exists()
assert SCRIPTS_OUTPUT_PATH.exists()


POSITIVES_PATH = COMPILATIONS_PATH / \
    "only_positives_for_q86_and_q870_between_2010_and_2019.csv"

df = load_negative_and_positive_df(NEGATIVES_PATH)
output = df.isna().mean()

with open(SCRIPTS_OUTPUT_PATH / 'missing_data_report.txt', 'w') as f:
    f.write(output.sort_values(ascending=False).to_string())

# # TODO: bad name, now used as input?
# NEGATIVES_PATH = SCRIPTS_OUTPUT_PATH / \
#     "eda_sample_stratified_on_2_percentage.csv"

# # TODO: bad name, now used as input?
# NEGATIVES_PATH = COMPILATIONS_PATH / "samples" / \
#     "5x_neutral_entries_0.csv"

# with open(SCRIPTS_OUTPUT_PATH / 'missing_data_report.txt', 'w') as f:
#     f.write(output.sort_values(ascending=False).to_string())

# pd.set_option('display.max_rows', None)

# for i in range(5):
#     print(f"Results for 5x_neutral_entries_{i}.csv")
#     NEGATIVES_PATH = COMPILATIONS_PATH / "samples" / \
#         f"5x_neutral_entries_{i}.csv"
#     df = load_negative_and_positive_df(NEGATIVES_PATH)
#     output = df.isna().mean()
#     print(output.sort_values(ascending=False))
#     print()
#     print("=======================================================")
#     print()


# end_time = time.time()
# print("Time elapsed: ", end_time - start_time, "seconds")
