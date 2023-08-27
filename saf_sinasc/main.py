# Meant to be run with `ipython -i` for exploration

import time
from saf_sinasc.models import default_run_models

import pandas as pd

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)


# TODO: remove ghosts, insert in a .env and make .sh and .py files use it.
# output_path="data/compilations/samples/5x_neutral_entries_$seed.csv";

start_time = time.time()
result = default_run_models(num_samples=100, save=True, use_seeds_file=True)
end_time = time.time()
elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time:.2f} seconds")
