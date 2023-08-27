import json

from saf_sinasc.scripts.config import SCRIPTS_OUTPUT_PATH

import json

# Read in the two input JSON files
with open(SCRIPTS_OUTPUT_PATH / 'total_lines_per_state.json') as f1:
    dict1 = json.load(f1)

with open(SCRIPTS_OUTPUT_PATH / 'check_sampling_eda_mechanism.json') as f2:
    dict2 = json.load(f2)

# Iterate over the keys in both dictionaries
output = {}
for key1 in dict1:
    output[key1] = {}
    for key2 in dict1[key1]:
        if ".xlsx" in key2:
            continue

        # Calculate the difference between the values in dict1 and dict2
        output[key1][key2] = dict1[key1][key2] - dict2[key1][key2]

with open(f"{SCRIPTS_OUTPUT_PATH}/difference_check_sampling_eda_mechanism.json", "w") as f:
    json.dump(output, f)
