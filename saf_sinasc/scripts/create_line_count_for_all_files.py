"""
This script is responsible only for gathering a count of
    how many lines each file of data has
    stratified by year and state.

This is intended to later be used to create a sample that respects
    this stratification, after multiplying by the adequate percentage for analysis.

Time elapsed:  6.694 seconds
"""

import json
import time

from subprocess import check_output
from glob import glob

from saf_sinasc.scripts.config import RAW_PATH, SCRIPTS_OUTPUT_PATH

start_time = time.time()

assert RAW_PATH.exists()
assert SCRIPTS_OUTPUT_PATH.exists()


def wc(filename):
    return int(check_output(["wc", "-l", filename]).split()[0])


output = {}

for f in glob(f"{RAW_PATH}/*/*", recursive=True):
    year, state = f.split("/")[-2:]
    if year not in output:
        output[year] = {}
    output[year][state] = wc(f)


with open(f"{SCRIPTS_OUTPUT_PATH}/total_lines_per_state.json", "w") as f:
    json.dump(output, f)

end_time = time.time()

print("Time elapsed: ", end_time - start_time, "seconds")
