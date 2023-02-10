"""
This script is responsible for using a total_lines count
    and then creating a dataset based on the percentage of each file

This script is not responsible for joining the sample with positive data
"""

import json
import time
import subprocess
import tempfile


from glob import glob
from pathlib import Path

from saf_sinasc.scripts.config import RAW_PATH, SCRIPTS_OUTPUT_PATH

start_time = time.time()

# TODO: bad name, fix in the other, maybe centralize as config
lines_per_file_path = SCRIPTS_OUTPUT_PATH / "total_lines_per_state.json"

assert RAW_PATH.exists()
assert SCRIPTS_OUTPUT_PATH.exists()
assert lines_per_file_path.exists()

# TODO am i using this
states_data = "../data/compilations/by_state"

SEED = 0
PERCENTAGE = 0.02
SAMPLE_PATH = SCRIPTS_OUTPUT_PATH / \
    f"eda_sample_stratified_on_{int(PERCENTAGE*100)}_percentage.csv"

# tail - n + 2 "$states_data/AC_2010_2019.csv" | shuf - -random-source = <(yes $seed) - n 95 >> "$output_path"


def create_header(path, output_file=SAMPLE_PATH):
    with open(output_file, 'w') as f:
        subprocess.run(["head", "-n", "1",  path], stdout=f)

# TODO: come on linter lint stuff


def concat_sample_data(path, lines_per_file, output_file=SAMPLE_PATH, seed=SEED, percentage=PERCENTAGE):
    year, state = path.split("/")[-2:]
    lines = lines_per_file[year][state]
    sample_size = int(lines * percentage)

    print(f"Read {path}, {lines} lines, sample size of: {sample_size}")

    # TODO dps ver oqq eh Popen e como ele eh difenrete e pq ele resolve isso
    tail = subprocess.Popen(["tail", "-n", "+2", path],
                            stdout=subprocess.PIPE)

    # Is there a way to create a tempfile for the session
    #    and just read it as needed in the random-seed?
    #   also, this doesn't solve things when I am in shellscrip so IDK
    # with tempfile.NamedTemporaryFile(mode='w') as temp:
    #     temp.write('\n'.join(['yes'] * seed))
    #     temp.seek(0)
    # f"--random-source={temp.name}",

    with open(output_file, 'a+') as f:
        shuf = subprocess.Popen(
            ["shuf",
                "-n", str(sample_size)],
            stdin=tail.stdout,
            stdout=f)
        tail.stdout.close()
        shuf.wait()

    # p1 = subprocess.run(["tail", "-n", "+2",  path],
    #                     capture_output=True)

    # with open(output_file, 'w+') as f:
    #     subprocess.run(
    #         ["shuf", p1.stdout, f"--random-source=<(yes {seed})", "-n", f"{sample_size}"], stdout=f)

    # print(p1)
    # print(p1.stdout)
    # tail -n +2 "$states_data/AC_2010_2019.csv" | shuf --random-source=<(yes $seed) -n 95   >> "$output_path";
    # como cacetes eu acerto isso?


with open(lines_per_file_path, 'r') as f:
    lines_per_file = json.load(f)


iterator = iter(glob(f"{RAW_PATH}/*/*", recursive=True))

first_path = next(iterator)

create_header(first_path)
concat_sample_data(first_path, lines_per_file)

for path in iterator:
    concat_sample_data(path, lines_per_file)


end_time = time.time()

print("Time elapsed: ", end_time - start_time, "seconds")


# Checking stuff
expected_line_count = sum(int(v2 * PERCENTAGE) for v1 in lines_per_file.values()
                          for v2 in v1.values()) + 1

actual_line_count = subprocess.run(
    ["wc", "-l",  SAMPLE_PATH], capture_output=True, text=True).stdout.split(" ")[0]

print(expected_line_count)
print(actual_line_count)
assert (expected_line_count == int(actual_line_count))

# TODO: tem 2 grandes coisas pra resolver nesse script ainda:
# 1) eu preciso appendar os positivos tambem
#       R: nao da, o header eh diferente
#           vai ter que ser no pandas essa parte.
#
# 2) eh BEM relevante ja ter seed nisso aqui, da pra ver como funca
#           (e ai eu ja posso ver como essas seed funciona maybe)
