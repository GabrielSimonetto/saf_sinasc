# Meant to be run with `ipython -i` for exploration

from saf_sinasc.models import run_models

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


run_models(
    run_dt=True, run_rf=True, run_xgb=True
)
