import ipdb
import json
import time
import subprocess
import tempfile


from glob import glob
from pathlib import Path

from saf_sinasc.scripts.config import SCRIPTS_OUTPUT_PATH, BY_STATE_PATH, COMPILATIONS_PATH


def find_ano_column_position(path):
    header = subprocess.check_output(
        ["head", "-n", "1", path]).decode().strip()

    return header.split(",").index("ANO")


def count_ano_lines(path, ano):
    ano_pos = find_ano_column_position(path)

    lines = subprocess.Popen(
        ["awk", "-F", ',', f'${ano_pos} == {ano}', path],
        stdout=subprocess.PIPE)

    count = subprocess.Popen(
        ["wc", "-l"],
        stdin=lines.stdout,
        stdout=subprocess.PIPE)

    # Capture the output of the `count` subprocess
    output, _ = count.communicate()

    # Convert the output to an integer
    count_int = int(output.strip())

    print(f"{path}: ANO: {ano}, {count_int}")

    return count_int


# # TODO: This ignores a single xlsx, intentionally
iterator = iter(glob(f"{BY_STATE_PATH}/*.csv", recursive=True))

# ipdb.set_trace()

output = {}

for path in iterator:
    state = path.split("/")[-1][:2]
    for ano in range(2010, 2020):
        if ano not in output:
            output[ano] = {}
        output[ano][f"SINASC-{state}-{ano}.csv"] = count_ano_lines(path, ano)

with open(f"{SCRIPTS_OUTPUT_PATH}/check_sampling_eda_mechanism.json", "w") as f:
    json.dump(output, f)

# actual_line_count = subprocess.run(
#     ["wc", "-l",  SAMPLE_PATH], capture_output=True, text=True).stdout.split(" ")[0]
