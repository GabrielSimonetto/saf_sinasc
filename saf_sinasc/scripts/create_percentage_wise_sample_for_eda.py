"""
This script is responsible for using a total_lines count
    and then creating a dataset based on the percentage of each file

This script is not responsible for joining the sample with positive data

Also, this sample stratifies data both by year, and state.
"""

import json
import time
import subprocess
import tempfile


from glob import glob
from pathlib import Path

from saf_sinasc.scripts.config import SCRIPTS_OUTPUT_PATH, BY_STATE_PATH

start_time = time.time()

# TODO: bad name, fix in the other, maybe centralize as config
lines_per_file_path = SCRIPTS_OUTPUT_PATH / "total_lines_per_state.json"

assert BY_STATE_PATH.exists()
assert SCRIPTS_OUTPUT_PATH.exists()
assert lines_per_file_path.exists()

SEED = 0
PERCENTAGE = 0.02
SAMPLE_PATH = (
    SCRIPTS_OUTPUT_PATH
    / f"eda_sample_stratified_on_{int(PERCENTAGE*100)}_percentage.csv"
)

# TODO: come on linter lint stuff


def create_header(path, output_file=SAMPLE_PATH):
    with open(output_file, "w") as f:
        subprocess.run(["head", "-n", "1", path], stdout=f)


def find_ano_column_position(path):
    header = subprocess.check_output(["head", "-n", "1", path]).decode().strip()

    return header.split(",").index("ANO")


# def get_ano_lines(path, ano):
#     ano_pos = find_ano_column_position(path)

#     # acho que vou enfiar isso junto na outra func
#     # tenho medo de como que esses treco lidam uns com os outros
#     #   se estiverem em funções separadas?
#     #   bom se eles sempre devem ser usados em conjunto eu ASSUMO que eles tem que ficar juntos mesmo
#     lines = subprocess.Popen(
#         ["awk", "-F", ',', f'${ano_pos} == {ano}', path],
#         stdout=subprocess.PIPE)

#     return lines


def concat_sample_data(
    path, lines_per_file, output_file=SAMPLE_PATH, seed=SEED, percentage=PERCENTAGE
):
    def get_sample_size(lines_per_file, ano, state, percentage):
        """
        ano: '2015',
        state: 'AP',

        needs to research
        "2015": {
          "SINASC-AP-2015.csv": 15751,
        }
        """

        state_file = f"SINASC-{state}-{ano}.csv"
        lines = lines_per_file[f"{ano}"][state_file]
        sample_size = int(lines * percentage)

        print(
            f"Read {path}, ano: {ano}, lines: {lines} , sample size of: {sample_size}"
        )
        return sample_size

    for ano in range(2010, 2020):
        ano_pos = find_ano_column_position(path)
        state = path.split("/")[-1][:2]
        sample_size = get_sample_size(lines_per_file, ano, state, percentage)

        awk = subprocess.Popen(
            ["awk", "-F", ",", f"${ano_pos} == {ano}", path], stdout=subprocess.PIPE
        )

        with open(output_file, "a+") as f:
            shuf = subprocess.Popen(
                ["shuf", "-n", str(sample_size)], stdin=awk.stdout, stdout=f
            )
            awk.stdout.close()
            shuf.wait()


with open(lines_per_file_path, "r") as f:
    lines_per_file = json.load(f)

# # TODO: This ignores a single xlsx, intentionally
iterator = iter(glob(f"{BY_STATE_PATH}/*.csv", recursive=True))

first_path = next(iterator)

create_header(first_path)
concat_sample_data(first_path, lines_per_file)

for path in iterator:
    concat_sample_data(path, lines_per_file)


end_time = time.time()

print("Time elapsed: ", end_time - start_time, "seconds")


# Checking stuff
expected_line_count = (
    sum(int(v2 * PERCENTAGE) for v1 in lines_per_file.values() for v2 in v1.values())
    + 1
)

actual_line_count = subprocess.run(
    ["wc", "-l", SAMPLE_PATH], capture_output=True, text=True
).stdout.split(" ")[0]

print(expected_line_count)
print(actual_line_count)
